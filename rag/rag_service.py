

import os
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# rag_service.py
from langchain_chroma import Chroma
from dotenv import load_dotenv  # load_dotenv'i burada da import edelim
import logging

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("rag_service")

# Modül yükleme mesajı
logger.info("Modül yükleniyor: {}".format(__file__))

# .env dosyasının tam yolunu manuel olarak belirtiyoruz.
# rag/rag_service.py'nin kendisi 'rag' klasörü içinde olduğu için,
# proje kök dizinine göre yolu hesaplamak için iki seviye yukarı çıkmalıyız.
project_root_for_rag = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path_for_rag = os.path.join(project_root_for_rag, ".env")
load_dotenv(dotenv_path=dotenv_path_for_rag)  # .env dosyasını manuel olarak yükle

logger.info(".env loaded from '{}'".format(dotenv_path_for_rag))

# API anahtarının yüklendiğinden emin olun
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    # Bu hata Streamlit'te gösterilecek.
    logger.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    raise ValueError("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")

# Vektör veritabanının kalıcı olarak saklanacağı dizin
# Bu dizini proje kök dizininde oluşturacağız.
PERSIST_DIRECTORY = os.path.join(
    project_root_for_rag, "chroma_db"
)  # <-- chroma_db yolunu da köke göre ayarla


def get_rag_retriever(data_directory: str = None):
    """
    RAG için retriever'ı başlatır.
    Veriler zaten ChromaDB'de varsa oradan yükler, yoksa yükler ve kaydeder.
    """
    logger.info("RAG retriever başlatılıyor. Veri dizini: {}".format(data_directory))

    # ÖNEMLİ: ChromaDB kalıcı olarak kaydedildiği için her çalıştırdığımızda yeniden oluşmasını engellemeliyiz.

    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        # Eğer ChromaDB veritabanı zaten varsa, yükle
        logger.info("ChromaDB '{}' konumundan yükleniyor.".format(PERSIST_DIRECTORY))
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings
        )
    else:
        # Eğer ChromaDB yoksa veya boşsa, veriyi yükle ve kaydet
        logger.info("ChromaDB bulunamadı veya boş. Veri yükleniyor ve kaydediliyor.")
        if not data_directory or not os.path.exists(data_directory):
            logger.error(
                "RAG için veri dizini '{}' bulunamadı. RAG devre dışı.".format(data_directory)
            )
            return None

        # Veriyi yükle - Hem TXT hem de PDF dosyalarını destekle
        # TXT dosyaları için loader - UTF-8 encoding ile
        txt_loader = DirectoryLoader(
            data_directory, 
            glob="**/*.txt", 
            loader_cls=lambda file_path: TextLoader(file_path, encoding="utf-8")
        )
        txt_documents = txt_loader.load()
        logger.info("{} TXT belgesi yüklendi.".format(len(txt_documents)))

        # PDF dosyaları için loader
        pdf_loader = DirectoryLoader(
            data_directory, glob="**/*.pdf", loader_cls=PyPDFLoader
        )
        pdf_documents = pdf_loader.load()
        logger.info("{} PDF belgesi yüklendi.".format(len(pdf_documents)))

        # Tüm belgeleri birleştir
        documents = txt_documents + pdf_documents
        logger.info("Toplam {} belge yüklendi.".format(len(documents)))

        # Metni parçalara ayır (chunking)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        logger.info("{} parça oluşturuldu.".format(len(texts)))

        # Embedding'leri oluştur ve ChromaDB'ye kaydet
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = Chroma.from_documents(
            documents=texts, embedding=embeddings, persist_directory=PERSIST_DIRECTORY
        )
        vectorstore.persist()  # Veritabanını kalıcı olarak diske yaz
        logger.info(
            "ChromaDB oluşturuldu ve '{}' konumuna kaydedildi.".format(PERSIST_DIRECTORY)
        )

    retriever = vectorstore.as_retriever()
    logger.info("RAG retriever başarıyla başlatıldı.")
    return retriever


def reset_chroma_db():
    """
    ChromaDB veritabanını sıfırlar. Yeni veri eklendiğinde veya veritabanı bozulduğunda kullanılabilir.
    """
    import shutil

    if os.path.exists(PERSIST_DIRECTORY):
        logger.warning("ChromaDB veritabanı siliniyor: {}".format(PERSIST_DIRECTORY))
        shutil.rmtree(PERSIST_DIRECTORY)
        logger.info(
            "ChromaDB veritabanı silindi. Bir sonraki çalıştırmada yeniden oluşturulacak."
        )
        return True
    return False
