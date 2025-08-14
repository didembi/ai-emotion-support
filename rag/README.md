# RAG (Retrieval-Augmented Generation) Servisi 📚

Bu modül, AI Emotion Support sisteminde kullanılan Retrieval-Augmented Generation (RAG) servisini içerir. RAG, büyük dil modellerinin (LLM) yanıtlarını iyileştirmek için harici bilgi kaynaklarını kullanma yöntemidir.

## 🌟 Özellikler

- **Bilgi Tabanlı Yanıtlar**: Duygusal destek yanıtlarını, stres yönetimi ve başa çıkma stratejileri gibi özel bilgi kaynaklarıyla zenginleştirir
- **Vektör Tabanlı Arama**: Google Generative AI Embeddings kullanarak semantik arama yapabilme
- **Kalıcı Vektör Veritabanı**: ChromaDB ile verileri kalıcı olarak saklama
- **Verimli Metin Parçalama**: Büyük metinleri anlamlı parçalara ayırma

## 🛠️ Teknik Detaylar

### Kullanılan Teknolojiler

- **LangChain**: Belge yükleme, metin parçalama ve vektör depolama için
- **Google Generative AI Embeddings**: Metin gömme (embedding) işlemleri için
- **ChromaDB**: Vektör veritabanı olarak
- **RecursiveCharacterTextSplitter**: Metinleri anlamlı parçalara bölmek için

### Veri Akışı

1. **Veri Yükleme**: Metin dosyaları `data/` dizininden yüklenir
2. **Metin Parçalama**: Büyük metinler daha küçük, anlamlı parçalara bölünür
3. **Embedding Oluşturma**: Her metin parçası için vektör gösterimleri oluşturulur
4. **Vektör Depolama**: Embeddingler ChromaDB'de saklanır
5. **Retrieval**: Kullanıcı sorguları ile ilgili en alakalı metin parçaları getirilir

## 🚀 Kullanım

RAG servisini kullanmak için:

```python
from rag.rag_service import get_rag_retriever

# RAG retriever'ı başlat
data_directory = "path/to/data"  # Veri dizini (örn: "data/")
retriever = get_rag_retriever(data_directory)

# Retriever'ı kullanarak ilgili belgeleri getir
documents = retriever.get_relevant_documents("stres yönetimi teknikleri")
```

## ⚙️ Yapılandırma

RAG servisi aşağıdaki ortam değişkenlerini kullanır:

- `GOOGLE_API_KEY`: Google Generative AI API anahtarı (gerekli)

## 📂 Veri Kaynakları

Sistem şu anda aşağıdaki veri kaynaklarını kullanmaktadır:

- `data/stress_management.txt`: Stres yönetimi ve başa çıkma stratejileri hakkında bilgiler

Yeni veri kaynakları eklemek için, `.txt` formatında dosyaları `data/` dizinine ekleyin ve servisi yeniden başlatın.

## 🔍 Sorun Giderme

- **ChromaDB Hataları**: Vektör veritabanı bozulursa, `chroma_db/` dizinini silip servisi yeniden başlatabilirsiniz
- **API Anahtarı Hataları**: `.env` dosyasında `GOOGLE_API_KEY` değişkeninin doğru ayarlandığından emin olun
- **Veri Yükleme Sorunları**: Veri dosyalarının UTF-8 formatında olduğundan emin olun

## 🔮 Gelecek Geliştirmeler

- Farklı dillerde veri desteği
- Daha fazla duygusal destek kaynağı ekleme
- Kullanıcı geri bildirimlerine göre retrieval kalitesini iyileştirme