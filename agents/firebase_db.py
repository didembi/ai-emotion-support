# ai-emotion-support/agents/firebase_db.py - SON VE KESİN KOD (DEBUG'SIZ, GÜVENLİ DAĞITIM İÇİN)
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import json # JSON içeriğini işlemek için

# .env dosyasının tam yolunu manuel olarak belirtiyoruz.
project_root_for_db = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path_for_db = os.path.join(project_root_for_db, '.env')
load_dotenv(dotenv_path=dotenv_path_for_db) 

# db istemcisi, initialize_firebase_app() tarafından atanacak.
db = None 

def initialize_firebase_app():
    """
    Firebase Admin SDK'yı başlatır ve Firestore istemcisini atar.
    Firebase Service Account JSON içeriğini doğrudan ortam değişkeninden (FIREBASE_CREDENTIALS) okur.
    """
    global db 

    if firebase_admin._apps:
        # Eğer uygulama zaten başlatılmışsa, mevcut Firestore istemcisini döndür.
        print("Firebase uygulaması zaten başlatılmış. Mevcut istemci döndürülüyor.")
        db = firestore.client()
        return db

    # Firebase kimlik bilgilerini doğrudan JSON string'inden alıyoruz
    # Bu değişkenin Streamlit Cloud'daki Secrets bölümünde veya .env'de (yerelde test için) tanımlı olduğundan emin olun.
    firebase_credentials_json_str = os.getenv("FIREBASE_CREDENTIALS") 
    
    if not firebase_credentials_json_str:
        print(f"HATA: 'FIREBASE_CREDENTIALS' ortam değişkeni (Streamlit Secrets'ta) tanımlı değil. Firebase başlatılamıyor.")
        db = None
        return None

    try:
        # JSON string'ini Python sözlüğüne dönüştür
        cred_dict = json.loads(firebase_credentials_json_str)
        cred = credentials.Certificate(cred_dict) # Dictionary'den kimlik bilgisi oluştur

        firebase_admin.initialize_app(cred)
        db = firestore.client() 
        print("Firebase bağlantısı başarılı!")
        return db # Başarılı durumda db istemcisini döndür
    except Exception as e:
        print(f"HATA: Firebase bağlantısı sırasında bir sorun oluştu: {e}")
        db = None
        return None

# --- CRUD Fonksiyonları ---
# Bu fonksiyonlar artık ilk argüman olarak bir db_client nesnesi alacak.
def save_conversation(db_client, user_id: str, conversation_entry: dict):
    if db_client: 
        try:
            doc_ref = db_client.collection('users').document(user_id).collection('conversations').document()
            doc_ref.set(conversation_entry)
            print(f"Konuşma başarıyla kaydedildi: {doc_ref.id}")
            return True
        except Exception as e:
            print(f"HATA: Konuşma kaydetme sırasında bir sorun oluştu: {e}")
            return False
    print(f"UYARI: Veritabanı istemcisi bulunamadığı için konuşma kaydedilemedi.")
    return False

def load_conversations(db_client, user_id: str) -> list:
    conversations = []
    if db_client: 
        try:
            docs = db_client.collection('users').document(user_id).collection('conversations').order_by('time', direction=firestore.Query.ASCENDING).stream()
            for doc in docs:
                entry = doc.to_dict()
                conversations.append(entry)
            print(f"{user_id} için {len(conversations)} konuşma yüklendi.")
        except Exception as e:
            print(f"HATA: Konuşma yükleme sırasında bir sorun oluştu: {e}")
    else:
        print(f"UYARI: Veritabanı istemcisi bulunamadığı için konuşmalar yüklenemedi.")
    return conversations

def delete_user_data(db_client, user_id: str):
    if db_client: 
        try:
            conv_ref = db_client.collection('users').document(user_id).collection('conversations')
            batch = db_client.batch()
            for doc in conv_ref.list_documents():
                batch.delete(doc)
            batch.commit()

            mood_ref = db_client.collection('users').document(user_id).collection('mood_history')
            batch = db_client.batch()
            for doc in mood_ref.list_documents():
                batch.delete(doc)
            batch.commit()
            
            db_client.collection('users').document(user_id).delete()
            print(f"Kullanıcı {user_id} verileri başarıyla silindi.")
            return True
        except Exception as e:
            print(f"HATA: Kullanıcı verisi silme sırasında bir sorun oluştu: {e}")
            return False
    print(f"UYARI: Veritabanı istemcisi bulunamadığı için kullanıcı verisi silinemedi.")
    return False

def save_mood_entry(db_client, user_id: str, mood_entry: dict):
    if db_client: 
        try:
            doc_ref = db_client.collection('users').document(user_id).collection('mood_history').document()
            doc_ref.set(mood_entry)
            print("Ruh hali başarıyla kaydedildi.")
            return True
        except Exception as e:
            print(f"HATA: Ruh hali kaydetme sırasında bir sorun oluştu: {e}")
            return False
    print(f"UYARI: Veritabanı istemcisi bulunamadığı için ruh hali kaydedilemedi.")
    return False

def load_mood_history(db_client, user_id: str) -> list:
    mood_history = []
    if db_client: 
        try:
            docs = db_client.collection('users').document(user_id).collection('mood_history').order_by('zaman', direction=firestore.Query.ASCENDING).stream()
            for doc in docs:
                entry = doc.to_dict()
                mood_history.append(entry)
            print(f"{user_id} için {len(mood_history)} ruh hali kaydı yüklendi.")
        except Exception as e:
            print(f"HATA: Ruh hali geçmişi yükleme sırasında bir sorun oluştu: {e}")
    else:
        print(f"UYARI: Veritabanı istemcisi bulunamadığı için ruh hali geçmişi yüklenemedi.")
    return mood_history