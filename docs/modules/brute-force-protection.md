# Brute Force Protection

## Purpose / Amaç
Bu modülün amacı, web uygulamalarına yönelik gerçekleştirilebilecek kaba kuvvet (brute force) parola tahmin saldırılarını engellemektir. Sistem; IP ve kullanıcı hesabı bazlı deneme sayısını takip ederek aşamalı gecikmeler, CAPTCHA doğrulaması ve nihayetinde hesabın geçici olarak kilitlenmesi gibi savunma mekanizmalarını devreye sokar.

## How It Works / Nasıl Çalışır
1. **Kullanıcı `/login` endpoint'ine istek atar:**
2. **Kilit kontrolü:** İlgili hesabın kilitli olup olmadığı Redis üzerinden kontrol edilir. Kilitliyse hesap anında reddedilir.
3. **CAPTCHA kontrolü (3+ denemede):** Eğer kullanıcı 3 veya daha fazla hatalı deneme yaptıysa, yeni isteklerde `captcha_token` zorunlu tutulur ve doğrulanır.
4. **Şifre doğrulama:** Gönderilen şifre kontrol edilir (örnekte "secret123" doğru kabul edilir).
5. **Aşamalı gecikme uygulanır:** Yanlış girişlerde hata sayısına bağlı olarak (0s, 2s, 10s) `time.sleep()` ile gecikme uygulanarak saldırgan yavaşlatılır.
6. **5+ denemede hesap kilitlenir + e-posta gönderilir:** Kullanıcı hesabı 15 dakika boyunca kilitlenir ve yetkiliye e-posta üzerinden otomatik olarak uyarı gönderilir. Başarılı bir girişte ise tüm bu sayaçlar sıfırlanır.

## Usage / Kullanım
Ortamı ayağa kaldırmak için terminalde şu komutu çalıştırın:
```bash
docker-compose up -d
```

Örnek cURL istekleri:
```bash
# Login (Başarısız / Başarılı)
curl -X POST http://localhost:8000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "ahmet", "password": "wrongpassword"}'

# Status Kontrolü
curl -X GET http://localhost:8000/status/ahmet

# Hesabın Kilidini Açma
curl -X POST http://localhost:8000/unlock/ahmet
```

## Output / Çıktı
Uygulama konsolunda gerçekleşen işlemlere dair örnek log formatları:
```text
[2024-01-01 12:00:00] IP=10.0.0.1 USER=ahmet ATTEMPT=#3 STATUS=FAILED
[2024-01-01 12:00:00] CAPTCHA verify -> token=mock-valid-token -> PASS
[2024-01-01 12:00:01] IP=10.0.0.1 USER=ahmet ATTEMPT=#5 STATUS=LOCKED
[2024-01-01 12:00:01] MOCK EMAIL -> Konu: [UYARI] Hesap Kilitlendi — ahmet
```

## Known Limitations / Bilinen Kısıtlamalar
- Uygulama şu an için **CAPTCHA** ve **E-posta** gönderimlerini *Mock Mode* (konsola yazdırma) üzerinden gerçekleştirmektedir.
- API güvenliği açısından gerçek bir projede muhakkak HTTPS / SSL sertifikası kullanımı şarttır.
