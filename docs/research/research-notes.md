# Araştırma Notları — Kaba Kuvvet Koruması

## Brute Force Saldırısı Nedir?

Saldırgan, doğru kimlik bilgilerini bulmak için sistematik olarak tüm
olası şifre kombinasyonlarını dener. Otomasyon araçları (Hydra, Burp Suite)
ile saniyede yüzlerce deneme yapılabilir.

## Aşamalı Gecikme (Progressive Delay)

Her başarısız denemede bekleme süresi artar:

| Deneme | Gecikme |
|--------|---------|
| 0–1    | 0 saniye |
| 2–3    | 2 saniye |
| 4      | 10 saniye |
| 5+     | Hesap kilidi (15 dk) |

**Neden etkili?** Saldırgan 1000 deneme yapmak istiyorsa:
- Gecikme olmadan: ~10 saniye
- Aşamalı gecikme ile: saatler

## IP Tabanlı vs Hesap Tabanlı Takip

| Yöntem | Avantaj | Dezavantaj |
|--------|---------|------------|
| IP tabanlı | VPN/proxy olmadan etkili | VPN ile atlatılabilir |
| Hesap tabanlı | VPN'den bağımsız | Meşru kullanıcı kilitlenebilir |
| İkisi birden | En kapsamlı koruma | Daha fazla Redis key |

## Redis Neden İdeal?

- `INCR` komutu atomik — race condition yok
- `EXPIRE` / `TTL` ile otomatik süre yönetimi
- In-memory olduğu için milisaniye yanıt süresi

## CAPTCHA Ne Zaman Devreye Girmeli?

3. başarısız denemeden sonra. Erken devreye girirse UX bozulur,
geç girerse bot çok deneme yapar.

## Kaynaklar

- OWASP Authentication Cheat Sheet
- Redis INCR Documentation
- Cloudflare Turnstile