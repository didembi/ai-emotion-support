# Kullanıcı Akışı – AI Destekli Duygu ve Kişisel Destek Kartı Uygulaması (Geliştirilmiş Sürüm)

Bu dosyada, kullanıcı deneyimi adım adım açıklanmıştır.  
Sistem, kullanıcının hem duygusunu hem de bu duyguya eşlik eden düşüncelerini ve ihtiyaçlarını analiz ederek kişisel destek mesajları üretir.


## 1. Açılış Ekranı

- Uygulama Streamlit tabanlı bir arayüzle açılır.
- Kullanıcıya karşılama mesajı gösterilir:
  _“Merhaba, bugün nasılsın? İçinden geçenleri benimle paylaşır mısın ?”_


## 2. Kullanıcı Girdileri (Form)

### a. Serbest Duygu / Durum Girişi
- Kullanıcı içinden geçenleri bir metin kutusuna yazar.  
  Örnek:  
  _“Bugün hiçbir şeye yetişemiyorum. Sanki sürekli yetersizim.”_

### b. Duygu Seçimi
- Kullanıcı o anki baskın duygusunu seçer (çoktan seçmeli):  
  **[Yalnızlık] [Stres] [Umutsuzluk] [Kızgınlık] [Korku] [Motivasyon Kaybı] [Diğer]**

### c. Duygu Şiddeti (1–5)
- Kullanıcı, yaşadığı duygunun şiddetini puanlar (slider bar):  
  _“Bu duyguyu ne kadar yoğun hissediyorsun?”_

### d. Zihinden Geçen Düşünce (Opsiyonel)
- Örnek:  
  _“Yine başaramadım.”, “Bana kimse değer vermiyor.”_

### e. O Anki İhtiyaç
- Kullanıcı, şu anda en çok neye ihtiyacı olduğunu belirtir:  
  **[Anlaşılmak] [Teselli] [Rahatlamak] [Yalnız Olmak] [Güç Toplamak] [Destek]**

---

## 3. NLP + Duygu Teması + İhtiyaç Analizi

- Sistem, kullanıcının yazdığı metni doğal dil işleme ile analiz eder.
- Belirtilen duygu, düşünce ve ihtiyaç bilgileriyle birlikte tema sınıflandırması yapılır.  
  (Örn: “Yetersizlik Hissi”, “Onay Arayışı”, “Tükenmişlik”)

---

## 4. Destek Mesajı Oluşturulması (Hibrit Model)

### a. Önceden Hazırlanmış Kartlar
- Uygulama, analize göre uygun destek kartlarını veri setinden seçer.

### b. AI ile Kişiselleştirme
- Seçilen kartlar referans alınarak, AI modeli (GPT / Claude) tarafından kullanıcının durumu ve ihtiyaçlarına özel bir destek mesajı üretilir.

---

## 5. Destek Mesajının Gösterimi

- Kullanıcıya üretilen cümle gösterilir.  
  Örnek:  
  _“Yetersiz hissettiğinde, bu duygunun senin değerinle ilgili olmadığını hatırla. Zaten elinden geleni yapıyorsun ve bu çok kıymetli.”_

- Kullanıcı aşağıdaki aksiyonları alabilir:
  - 💾 “Kaydet”  
  - 🔁 “Yeniden üret”  
  - ✅ “Bana iyi geldi”  
  - 📋 “Günlüğüme ekle”


## 6. Günlük ve Geçmiş Mesajlar (Geliştiriliebilir)

- Kullanıcı daha önce aldığı destek mesajlarını bir günlük görünümünde görebilir.
- İsterse belirli mesajlara not ekleyebilir veya favori olarak işaretleyebilir.


## 7. Oturumu Sonlandırma

- Kullanıcı yeni bir giriş yapmak isteyebilir veya oturumu sonlandırabilir.
- Veriler isteğe bağlı olarak SQLite veya PostgreSQL veritabanında saklanır.
