import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL_ALERT_TO = os.getenv("EMAIL_ALERT_TO", "admin@example.com")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

def _send_email(subject: str, body: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER or "alert@bruteforce.local"
        msg['To'] = EMAIL_ALERT_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_HOST, int(SMTP_PORT))
        server.starttls()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"[{timestamp}] EMAIL SENT -> Alıcı: {EMAIL_ALERT_TO}")
    except Exception as e:
        print(f"[{timestamp}] EMAIL ERROR -> {str(e)}")

def send_lock_alert(username: str, ip: str, attempt_count: int) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"[UYARI] Hesap Kilitlendi — {username}"
    body = f"""Kullanıcı: {username}
IP Adresi: {ip}
Deneme Sayısı: {attempt_count}
Kilitlenme Zamanı: {timestamp}
Kilit Süresi: 15 dakika
"""
    
    if not SMTP_HOST:
        print(f"[{timestamp}] MOCK EMAIL -> Konu: {subject}")
        print(f"[{timestamp}] MOCK EMAIL -> Alıcı: {EMAIL_ALERT_TO}")
        print(f"[{timestamp}] MOCK EMAIL -> IP: {ip} | Deneme: {attempt_count}")
        return
        
    _send_email(subject, body)

def send_unlock_alert(username: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"[BİLGİ] Hesap Kilidi Açıldı — {username}"
    body = f"""Kullanıcı: {username}
Zaman: {timestamp}
"""
    
    if not SMTP_HOST:
        print(f"[{timestamp}] MOCK EMAIL -> Konu: {subject}")
        print(f"[{timestamp}] MOCK EMAIL -> Alıcı: {EMAIL_ALERT_TO}")
        print(f"[{timestamp}] MOCK EMAIL -> Hesap kilidi açıldı: {username}")
        return
        
    _send_email(subject, body)
