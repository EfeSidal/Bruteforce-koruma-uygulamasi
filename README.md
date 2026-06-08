<div align="center">
  <a href="https://istinye.edu.tr">
    <img src="docs/assets/istinye-university-logo.png" alt="Istinye University" width="180"/>
  </a>

  # Kaba Kuvvet Koruması — Brute Force Protection

  ![GitHub](https://img.shields.io/badge/GitHub-Private-red?style=flat-square&logo=github)
  ![Language](https://img.shields.io/badge/Language-Python-blue?style=flat-square)
  ![Status](https://img.shields.io/badge/Status-Completed-green?style=flat-square)
  ![Course](https://img.shields.io/badge/Course-BGT208-purple?style=flat-square)
  ![License](https://img.shields.io/badge/License-Educational-green?style=flat-square)
</div>

---

## 🎓 Instructor / Danışman

| | |
|---|---|
| **Name / Ad** | Keyvan Arasteh |
| **GitHub** | [@keyvanarasteh](https://github.com/keyvanarasteh) |
| **Email** | [keyvan.arasteh@istinye.edu.tr](mailto:keyvan.arasteh@istinye.edu.tr) |
| **LinkedIn** | [keyvanarasteh](https://www.linkedin.com/in/keyvanarasteh/) |
| **Website** | [qline.tech](https://qline.tech) |

---

## 👤 Student / Öğrenci

| | |
|---|---|
| **Name / Ad Soyad** | Efe Sidal |
| **Student ID / Öğrenci No** | `2420****1004` |

---

## 📚 Course Information / Ders Bilgileri

| | |
|---|---|
| **Course Name / Ders Adı** | Secure Web Development / Güvenli Web Yazılımı Geliştirme |
| **Course Code / Ders Kodu** | BGT208 |
| **Credits / Kredi** | 3 ECTS |
| **Semester / Dönem** | 2025-2026 Spring / 2025-2026 Bahar |
| **Institution / Üniversite** | [Istinye University](https://istinye.edu.tr) |

---

## 📋 Project Overview / Proje Özeti

FastAPI, Redis ve Docker kullanılarak geliştirilmiş aşamalı kaba kuvvet koruma sistemi. BGT208 — Güvenli Web Yazılımı Geliştirme dersi kapsamında implement edilmiştir.

Sistem şu özellikleri içerir:
- Aşamalı gecikme: 0s → 2s → 10s → hesap kilidi (5+ denemede)
- IP tabanlı ve hesap tabanlı deneme takibi (Redis)
- 3+ denemede CAPTCHA doğrulaması (Cloudflare Turnstile mock)
- Hesap kilitlenince otomatik e-posta uyarısı (mock SMTP)
- Kilit açma mekanizması (/unlock endpoint)
- Saldırı simülasyon scripti ve log çıktısı

---

## 🗂 Repository Structure / Repo Yapısı

```
.
├── README.md
├── ROADMAP.md
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── docs/
│   ├── modules/
│   │   └── brute-force-protection.md
│   ├── research/
│   └── references/
└── src/
    ├── main.py
    ├── counter.py
    ├── delay_policy.py
    ├── captcha.py
    ├── alert.py
    └── simulator.py
```

---

## 🚀 Getting Started / Kurulum

```bash
git clone https://github.com/efesidal/bruteforce
cd bruteforce
cp .env.example .env
# Edit .env with your values / .env dosyasını doldurun
docker-compose up -d
```

---

## 📊 Deliverables / Teslimler

| Item | Status |
|------|--------|
| Koruma sistemi (`src/`) | ✅ |
| Saldırı simülasyon logu | ✅ |
| Kilit açma + e-posta uyarısı | ✅ |

---

## 📚 Documentation / Belgeleme

All module docs → [`docs/modules/`](./docs/modules/)
Research notes → [`docs/research/`](./docs/research/)

---

## 🔗 References / Kaynaklar

- [OWASP Brute Force Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Redis Documentation — INCR command](https://redis.io/commands/incr/)
- [Cloudflare Turnstile Docs](https://developers.cloudflare.com/turnstile/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)