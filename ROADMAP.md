# ROADMAP

## Proje Aşamaları

- Phase 0: ✅ tamamlandı — brute force, redis, rate limiting araştırıldı
- Phase 1: ✅ tamamlandı — docs/research/ notları
- Phase 2: ✅ tamamlandı — Docker + Redis kuruldu
- Phase 3: ✅ tamamlandı — 5 modül implement edildi
- Phase 4: ✅ tamamlandı — simülasyon testi yapıldı, loglar üretildi
- Phase 5: ⬜ — README tamamlanacak, hoca collaborator eklenecek

## What I Learned
- **Redis INCR + TTL kombinasyonunun atomik sayaç için neden ideal olduğu:** Her istekte veritabanı performansından kayıp yaşamadan hızlıca okuma/yazma işlemi yapabilmek ve eşzamanlı isteklerde yarış durumu (race condition) yaşamamak için Redis'in `INCR` (atomik artırma) ve `TTL` mekanizmaları kilit role sahiptir.
- **Aşamalı gecikmenin UX ve güvenlik dengesini nasıl sağladığı:** Birkaç ufak denemede kullanıcıyı doğrudan engellemek yerine önce kısa bir gecikme eklemek ve ancak ciddi (ve şüpheli) denemelerde uzun cezalar/kilitler vermek, gerçek kullanıcıların (UX) mağdur olmasını engellerken otomatik botları büyük ölçüde etkisiz hale getirir.
- **Docker multi-service kurulumunda servisler arası iletişim:** Tüm modüllerin (`app` ve `redis`) izole ağlarda sorunsuz çalışabilmesi ve `.env` dosyasıyla ortam değişkenleri üzerinden diğer servislere başarıyla bağlanabilmesi detaylıca öğrenildi.
