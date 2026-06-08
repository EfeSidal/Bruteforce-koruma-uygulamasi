from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime

from src.counter import (
    increment_attempt,
    get_attempt_count,
    lock_account,
    is_locked,
    reset_attempts
)
from src.delay_policy import apply_delay, should_lock
from src.captcha import is_captcha_required, verify_captcha

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str
    captcha_token: Optional[str] = None

def log_attempt(ip: str, username: str, attempt: int, status: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] IP={ip} USER={username} ATTEMPT=#{attempt} STATUS={status}")

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/login")
def login(login_data: LoginRequest, request: Request):
    username = login_data.username
    password = login_data.password
    ip = request.client.host if request.client else "unknown"
    
    lock_key = f"lock:{username}"
    account_key = f"account:{username}"
    ip_key = f"ip:{ip}"
    
    # 1. Kilit kontrolü
    if is_locked(lock_key):
        attempt_count = get_attempt_count(account_key)
        log_attempt(ip, username, attempt_count, "LOCKED")
        return {"success": False, "message": "Hesap kilitli. 15 dakika bekleyin."}
    
    # 1.5 CAPTCHA kontrolü
    attempt_count = get_attempt_count(account_key)
    if is_captcha_required(attempt_count):
        if not login_data.captcha_token:
            return {
                "success": False,
                "captcha_required": True,
                "message": "CAPTCHA doğrulaması gerekli."
            }
        
        if not verify_captcha(login_data.captcha_token):
            return {
                "success": False,
                "captcha_required": True,
                "message": "Geçersiz CAPTCHA."
            }

    # 2. Şifre doğrulama (Test için: "secret123")
    if password != "secret123":
        # Yanlış şifre durumu
        increment_attempt(ip_key)
        account_attempts = increment_attempt(account_key)
        
        # Gecikme uygula
        apply_delay(account_attempts)
        
        # Kilitlenmesi gerekiyor mu?
        if should_lock(account_attempts):
            lock_account(lock_key, 900)  # 15 dakika = 900 saniye
            log_attempt(ip, username, account_attempts, "LOCKED")
            return {
                "success": False, 
                "attempt": account_attempts, 
                "message": "Çok fazla hatalı deneme. Hesap kilitlendi."
            }
        
        log_attempt(ip, username, account_attempts, "FAILED")
        return {
            "success": False, 
            "attempt": account_attempts, 
            "message": "Hatalı şifre."
        }
    
    # 3. Doğru şifre durumu
    reset_attempts(ip_key)
    reset_attempts(account_key)
    log_attempt(ip, username, 0, "OK")
    
    return {"success": True, "message": "Giriş başarılı."}

@app.get("/status/{username}")
def get_status(username: str):
    account_key = f"account:{username}"
    lock_key = f"lock:{username}"
    
    attempts = get_attempt_count(account_key)
    locked = is_locked(lock_key)
    
    return {
        "username": username,
        "attempts": attempts,
        "locked": locked
    }

@app.post("/unlock/{username}")
def unlock_account(username: str):
    account_key = f"account:{username}"
    lock_key = f"lock:{username}"
    
    reset_attempts(account_key)
    reset_attempts(lock_key)  # reset_attempts redis_client.delete() yapıyor
    
    return {"message": f"Hesap kilidi açıldı: {username}"}
