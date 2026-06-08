# ROADMAP — Kaba Kuvvet Koruması
# ROADMAP — Brute Force Protection

> Course / Ders: Secure Web Development (BGT208) · Istinye University
> Instructor / Danışman: Keyvan Arasteh

---

## Phase 0 / Faz 0: Understand Before You Build / Yazmadan Önce Anla

Before writing a single line of code, I answered these questions:
Tek satır kod yazmadan önce şu soruları yanıtladım:

- What is the project? / Proje nedir?
  Brute force saldırılarına karşı aşamalı gecikme, kilitleme ve CAPTCHA içeren koruma sistemi.
- How does it work? / Nasıl çalışır?
  Redis ile deneme sayısı tutulur, aşamalı gecikme uygulanır, 5+ denemede hesap kilitlenir.
- What are the inputs/outputs? / Girdiler/çıktılar neler?
  Girdi: kullanıcı adı + şifre. Çıktı: başarı/hata mesajı, gecikme, kilit durumu, log.
- What tools will I use and why? / Hangi araçları kullanacağım ve neden?
  Python + FastAPI (hızlı REST API), Redis (atomik sayaç + TTL), Docker (izole ortam).

---

## Phase 1 / Faz 1: Research & Investigation / Araştırma ve Keşif

> Folder / Klasör: `docs/research/`

| Topic / Konu | Status / Durum | Notes / Notlar |
|--------------|----------------|----------------|
| Brute force saldırısı anatomisi | ✅ Tamamlandı | docs/research/research-notes.md |
| Redis INCR + TTL ile atomik sayaç | ✅ Tamamlandı | docs/research/research-notes.md |
| IP tabanlı vs hesap tabanlı takip | ✅ Tamamlandı | docs/research/research-notes.md |
| CAPTCHA entegrasyonu (Turnstile) | ✅ Tamamlandı | docs/research/research-notes.md |
| Aşamalı gecikme stratejisi | ✅ Tamamlandı | docs/research/research-notes.md |

---

## Phase 2 / Faz 2: Environment Setup / Ortam Kurulumu

- [x] Isolated lab environment (Docker / VM) / İzole lab ortamı
- [x] Tools installed and verified / Araçlar kuruldu ve test edildi
- [x] `.env.example` created / oluşturuldu

---

## Phase 3 / Faz 3: Implementation / Uygulama

### Module / Modül: Brute Force Protection

1. Redis sayaç modülü (counter.py) — IP + hesap bazlı INCR, TTL, lock
2. Aşamalı gecikme politikası (delay_policy.py) — 0s → 2s → 10s → kilit
3. FastAPI endpointleri (main.py) — /login, /status, /unlock
4. CAPTCHA middleware (captcha.py) — 3+ denemede mock Turnstile doğrulama
5. E-posta uyarı sistemi (alert.py) — kilitlenince mock SMTP bildirimi

---

## Phase 4 / Faz 4: Testing & Reporting / Test ve Raporlama

- [x] Ran tests against target/sample / Hedef/örnek üzerinde testler çalıştırıldı
- [x] Documented all findings with evidence / Tüm bulgular kanıtlarıyla belgelendi
- [x] Wrote final report (Markdown) / Final raporu yazıldı — docs/modules/brute-force-protection.md

---

## Phase 5 / Faz 5: Delivery / Teslim

- [x] GitHub repository is clean and organized / Repo temiz ve düzenli
- [x] README.md complete / eksiksiz
- [x] Docker verified (`docker-compose up`) / doğrulandı
- [ ] Instructor invited as collaborator / Danışman collaborator olarak eklendi → **keyvanarasteh**

---

## What I Learned / Öğrendiklerim

- Redis'in `INCR` + `EXPIRE` kombinasyonu, race condition olmadan atomik sayaç tutmak için idealdir.
- Aşamalı gecikme, UX'i bozmadan bot saldırılarını yavaşlatmanın en etkili yollarından biridir.
- Docker Compose ile çoklu servis kurulumunda servisler arası iletişim için ortak network tanımı şarttır.
- IP tabanlı takip tek başına yetersizdir; VPN kullanan saldırganlara karşı hesap bazlı takip zorunludur.
- CAPTCHA'yı çok erken devreye almak (1. denemede) kullanıcı deneyimini ciddi ölçüde bozar.