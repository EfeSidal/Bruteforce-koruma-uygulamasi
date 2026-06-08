import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def increment_attempt(key: str) -> int:
    """
    Redis'te key'i 1 artırır. İlk denemede TTL 1 saat olarak atanır.
    """
    count = redis_client.incr(key)
    if count == 1:
        # 1 saat = 3600 saniye
        redis_client.expire(key, 3600)
    return count

def get_attempt_count(key: str) -> int:
    """
    Mevcut deneme sayısını döndürür. Key yoksa 0 döner.
    """
    count = redis_client.get(key)
    if count is None:
        return 0
    return int(count)

def lock_account(key: str, duration: int) -> None:
    """
    Hesabı belirli bir süre (duration) kilitler. Değer "locked" olarak ayarlanır.
    """
    redis_client.set(key, "locked", ex=duration)

def is_locked(key: str) -> bool:
    """
    Hesabın kilitli olup olmadığını kontrol eder.
    """
    val = redis_client.get(key)
    return val == "locked"

def reset_attempts(key: str) -> None:
    """
    Belirtilen key'i siler. Başarılı giriş sonrasında kullanılabilir.
    """
    redis_client.delete(key)

if __name__ == "__main__":
    test_account_key = "account:testuser"
    test_lock_key = "lock:testuser"
    
    print("--- Redis Sayaç Modülü Testi Başlıyor ---")
    
    # 1. Ortamı temizle
    reset_attempts(test_account_key)
    reset_attempts(test_lock_key)
    print("- Önceki veriler temizlendi.")
    
    # 2. İlk deneme sayısını kontrol et
    initial_count = get_attempt_count(test_account_key)
    print(f"- Başlangıç deneme sayısı: {initial_count} (Beklenen: 0)")
    
    # 3. İki kere yanlış deneme yap (increment)
    c1 = increment_attempt(test_account_key)
    print(f"- 1. Yanlış giriş sonrası deneme sayısı: {c1} (Beklenen: 1)")
    c2 = increment_attempt(test_account_key)
    print(f"- 2. Yanlış giriş sonrası deneme sayısı: {c2} (Beklenen: 2)")
    
    # 4. Hesabın kilitli olup olmadığını kontrol et
    locked_initial = is_locked(test_lock_key)
    print(f"- Hesap şu an kilitli mi?: {locked_initial} (Beklenen: False)")
    
    # 5. Hesabı 60 saniyeliğine kilitle
    lock_account(test_lock_key, 60)
    print(f"- {test_lock_key} keyi ile hesap 60 saniyeliğine kilitlendi.")
    
    # 6. Hesabın kilitlendiğini doğrula
    locked_after = is_locked(test_lock_key)
    print(f"- Hesap şu an kilitli mi?: {locked_after} (Beklenen: True)")
    
    # 7. Başarılı giriş durumunu simüle et (reset)
    reset_attempts(test_account_key)
    final_count = get_attempt_count(test_account_key)
    print(f"- Sıfırlama işleminden sonra deneme sayısı: {final_count} (Beklenen: 0)")
    
    # Testleri bitirip çöpleri temizle
    reset_attempts(test_account_key)
    reset_attempts(test_lock_key)
    print("--- Redis Sayaç Modülü Testi Bitti ---")
