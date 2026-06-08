from datetime import datetime

CAPTCHA_THRESHOLD = 3

def is_captcha_required(attempt_count: int) -> bool:
    """
    Belirli bir deneme sayısını (CAPTCHA_THRESHOLD) aşan durumlar için
    CAPTCHA doğrulamasının gerekli olup olmadığını döner.
    """
    return attempt_count >= CAPTCHA_THRESHOLD

def verify_captcha(token: str) -> bool:
    """
    Gelen CAPTCHA token'ını doğrular (Mock modunda çalışır).
    Sadece 'mock-valid-token' değeri kabul edilir.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if token == "mock-valid-token":
        print(f"[{timestamp}] CAPTCHA verify -> token={token} -> PASS")
        return True
    else:
        print(f"[{timestamp}] CAPTCHA verify -> token={token} -> FAIL")
        return False
