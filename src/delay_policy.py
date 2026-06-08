import time
from datetime import datetime

def get_delay(attempt_count: int) -> float:
    """
    Deneme sayısına göre beklenecek süreyi (saniye) döndürür.
    0-1 deneme -> 0 saniye
    2-3 deneme -> 2 saniye
    4 deneme   -> 10 saniye
    5+ deneme  -> -1 döndür (kilit sinyali)
    """
    if attempt_count <= 1:
        return 0.0
    elif 2 <= attempt_count <= 3:
        return 2.0
    elif attempt_count == 4:
        return 10.0
    else:
        return -1.0

def should_lock(attempt_count: int) -> bool:
    """
    Deneme sayısı 5 veya daha fazlaysa True döndürür.
    """
    return attempt_count >= 5

def apply_delay(attempt_count: int, sleep_multiplier: float = 1.0) -> None:
    """
    Gecikmeyi hesaplar ve uygular. Kilit durumu yoksa time.sleep() ile geciktirir.
    Test amaçlı sleep sürelerini azaltmak için sleep_multiplier parametresi kullanılabilir.
    """
    delay = get_delay(attempt_count)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if delay == -1.0:
        print(f"[{current_time}] attempt #{attempt_count} -> LOCKED")
    else:
        # Eğer delay float görünümündeyse int'e dönüştürüp temiz yazdıralım (örn: 2.0 -> 2)
        formatted_delay = int(delay) if delay.is_integer() else delay
        print(f"[{current_time}] attempt #{attempt_count} -> delay: {formatted_delay}s")
        if delay > 0:
            time.sleep(delay * sleep_multiplier)

if __name__ == "__main__":
    print("--- Gecikme Politikası Modülü Testi Başlıyor ---")
    # 0'dan 6'ya kadar her deneme için test et
    for i in range(7):
        # sleep_multiplier=0.1 ile bekleme sürelerini 10'da 1'ine düşürüyoruz
        apply_delay(i, sleep_multiplier=0.1)
    print("--- Gecikme Politikası Modülü Testi Bitti ---")
