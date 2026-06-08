import time
import datetime
import requests
import sys

BASE_URL = "http://localhost:8000"
LOG_FILE = "attack_simulation.log"

stats = {
    "s1_attempts": 0, "s1_locks": 0,
    "s2_attempts": 0, "s2_locks": 0,
    "s3_attempts": 0, "s3_success": 0,
    "total_requests": 0
}

def log_msg(msg: str):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def unlock_user(username: str):
    try:
        requests.post(f"{BASE_URL}/unlock/{username}", timeout=5)
    except Exception as e:
        print(f"Hata: {e}")

def attempt_login(scenario: int, ip: str, username: str, password: str, attempt_num: int, captcha_token: str = None) -> dict:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headers = {"X-Forwarded-For": ip}
    payload = {"username": username, "password": password}
    if captcha_token:
        payload["captcha_token"] = captcha_token

    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload, headers=headers, timeout=10)
        delay = round(time.time() - start_time, 2)
        data = response.json()
        
        status = "FAILED"
        if data.get("success"):
            status = "OK"
        elif "kilitli" in data.get("message", "").lower():
            status = "LOCKED"
            
        log_msg(f"[{timestamp}] SENARYO={scenario} IP={ip} USER={username} ATTEMPT=#{attempt_num} DELAY={delay}s STATUS={status}")
        stats["total_requests"] += 1
        return data
    except Exception as e:
        log_msg(f"[{timestamp}] SENARYO={scenario} IP={ip} USER={username} ATTEMPT=#{attempt_num} ERROR={e}")
        return {}

def run_scenario_1():
    scenario = 1
    ip = "10.0.0.1"
    user = "victim1"
    unlock_user(user)
    
    for i in range(1, 9):
        stats["s1_attempts"] += 1
        # 3. denemeden itibaren captcha isteyecek
        captcha = "mock-valid-token" if i >= 3 else None
        res = attempt_login(scenario, ip, user, "wrongpass", i, captcha_token=captcha)
        if "kilitli" in res.get("message", "").lower():
            stats["s1_locks"] = 1

def run_scenario_2():
    scenario = 2
    ips = ["10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6"]
    user = "victim2"
    unlock_user(user)
    
    attempt_num = 1
    for ip in ips:
        for _ in range(2):
            stats["s2_attempts"] += 1
            captcha = "mock-valid-token" if attempt_num >= 3 else None
            res = attempt_login(scenario, ip, user, "wrongpass", attempt_num, captcha_token=captcha)
            if "kilitli" in res.get("message", "").lower():
                stats["s2_locks"] = 1
            attempt_num += 1

def run_scenario_3():
    scenario = 3
    ip = "10.0.0.7"
    user = "victim3"
    unlock_user(user)
    
    # 2 wrong
    for i in range(1, 3):
        stats["s3_attempts"] += 1
        attempt_login(scenario, ip, user, "wrongpass", i)
        
    # 1 success
    stats["s3_attempts"] += 1
    res = attempt_login(scenario, ip, user, "secret123", 3)
    if res.get("success"):
        stats["s3_success"] = 1
        
    # Verify via status
    try:
        r = requests.get(f"{BASE_URL}/status/{user}", timeout=5)
        d = r.json()
        log_msg(f"[STATUS CHECK] USER={user} ATTEMPTS={d.get('attempts')} LOCKED={d.get('locked')}")
    except Exception as e:
        pass

if __name__ == "__main__":
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== BRUTE FORCE SIMULATION LOG ===\n")
        
    log_msg("Simülasyon başlıyor...\n")
    
    run_scenario_1()
    log_msg("")
    run_scenario_2()
    log_msg("")
    run_scenario_3()
    log_msg("")
    
    log_msg("======= SİMÜLASYON ÖZETI =======")
    log_msg(f"Senaryo 1: {stats['s1_attempts']} deneme, {stats['s1_locks']} kilit")
    log_msg(f"Senaryo 2: {stats['s2_attempts']} deneme, {stats['s2_locks']} kilit")
    log_msg(f"Senaryo 3: {stats['s3_attempts']} deneme, başarılı giriş")
    log_msg(f"Toplam istek: {stats['total_requests']}")
    log_msg("================================")
