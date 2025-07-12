# Teknoloji Yığını – AI Destekli Duygu ve Kişisel Destek Mesajı Uygulaması

Bu belge, kullanıcıdan duygusal veri alarak AI ile kişisel destek cümleleri üreten uygulamanın geliştirilmesinde kullanılacak programlama dillerini, kütüphaneleri ve araçları özetler.

---

## Frontend

| Araç           | Amacı                                                                 |
|--------------  |------------------------------------------------------------------------|
| **Streamlit**  | Kullanıcının duygu/düşüncelerini girdiği ve AI destek mesajını aldığı etkileşimli web arayüzünü oluşturmak |
| **HTML/CSS** (Streamlit üzerinden) | Streamlit kendi içinde basit bir tasarım sağlar; ekstra stil gerekirse HTML/CSS ile özelleştirilebilir |

---

##  Backend & Yapay Zekâ

| Araç / Kütüphane                | Amacı                                                                 |
|----------------------           |------------------------------------------------------------------------|
| **Python**                      | Uygulamanın temel programlama dili                                     |
| **OpenAI API / Claude**         | Kullanıcının girdisine göre kişisel destek cümlesi üreten Büyük Dil Modeli (LLM) |
| **NLTK / spaCy** (isteğe bağlı) | Duygu analizi ve metin ön işleme için NLP araçları (kullanılacaksa)         |
| **Prompt Engineering**          | AI'yi daha doğru yönlendirmek için yapılandırılmış girdiler oluşturmak (örneğin: duygu+şiddet+ihtiyaç bilgisiyle mesaj üretimi) |

---

##  Veri Saklama ve Yönetimi

| Araç                           | Amacı                                                                 |
|--------------------------------|------------------------------------------------------------------------|
| **SQLite**                     | Basit günlük kaydı ve mesaj saklama için hafif bir yerel veritabanı    |
| **PostgreSQL** (opsiyonel)     | Daha büyük ölçekli veri yönetimi için kullanılabilir (örneğin kullanıcı tabanlı günlük geçmişi) |

---

##  Ortam Yönetimi

| Araç           | Amacı                                                                 |
|----------------|------------------------------------------------------------------------|
| **dotenv**     | API anahtarlarını ve gizli verileri .env dosyasıyla güvenli şekilde yönetmek |
| **venv**       | Sanal ortam oluşturarak proje bağımlılıklarını izole etmek             |
| **requirements.txt** | Projeye ait tüm kütüphaneleri ve sürümlerini takip etmek için kullanılır  |

---

##  Sürüm Kontrolü ve Kod Yönetimi

| Araç         | Amacı                                                                 |
|--------------|------------------------------------------------------------------------|
| **GitHub**   | Projenin çevrim içi olarak paylaşımı, iş birliği ve teslimat yönetimi  |

---

## 🛠 Ek Araçlar (İsteğe Bağlı / Gelecekteki Geliştirmeler)

| Araç / Teknoloji           | Amacı                                                                 |
|------------------------ ---|------------------------------------------------------------------------|
| **Text-to-Speech (TTS)**   | Kullanıcının mesajı sesli olarak dinleyebilmesini sağlamak            |
| **LangChain / LlamaIndex** | LLM'yi daha verimli çalıştırmak için gelişmiş bağlam yönetimi        |
| **Streamlit SessionState** | Oturum bilgisi veya günlük mesaj takibi gibi geçici verileri yönetmek |

---

## 💻 Geliştirme Ortamı

- Python 
- Streamlit 
