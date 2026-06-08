# Kaba Kuvvet Koruması — Brute Force Protection

![Python](https://img.shields.io/badge/Language-Python-blue)

## Project Overview
Aşamalı gecikme, kilitleme ve CAPTCHA içeren brute force koruma sistemi. FastAPI + Redis + Docker ile implement edildi. Sistem; kullanıcıların yanlış parola denemelerini Redis üzerinde atomik olarak tutarak aşamalı bekletme sürelerini uzatır, bot girişimlerini yavaşlatır ve 5. denemeden sonra hesabı kilit altına alarak sistem yöneticisine e-posta ile otomatik uyarı gönderir.

## Deliverables
| Teslimatlar | Durum |
|---|---|
| Koruma sistemi (`src/`) | ✅ |
| Saldırı simülasyon logu | ✅ |
| Kilit açma + e-posta uyarısı | ✅ |

## References
- [OWASP Brute Force Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Redis Documentation — INCR command](https://redis.io/commands/incr/)
- [Cloudflare Turnstile Docs](https://developers.cloudflare.com/turnstile/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---
**Öğrenci Adı Soyadı:** [Placeholder - Efe Sidal]  
**Öğrenci No:** [Placeholder]  
**Ders:** BGT208 Secure Web Development
