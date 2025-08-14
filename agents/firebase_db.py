# ai-emotion-support/agents/firebase_db.py - YEREL DEBUG İÇİN GEÇİCİ KOD (Tüm Debuglar Dahil)
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import json 

print(f"--- DEBUG (firebase_db.py): Modül yükleniyor: {__file__} ---")

# .env dosyasının tam yolunu manuel olarak belirtiyoruz.
project_root_for_db = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path_for_db = os.path.join(project_root_for_db, '.env')
load_dotenv(dotenv_path=dotenv_path_for_db) 

print(f"DEBUG (firebase_db.py): .env loaded from '{dotenv_path_for_db}'.")

# Global db nesnesi. Başlangıçta None, initialize_firebase_app() tarafından atanacak.
db = None 

def initialize_firebase_app():
    global db 
    print(f"DEBUG (firebase_db.py): initialize_firebase_app fonksiyonu çağrıldı.")

    if firebase_admin._apps:
        print("DEBUG (firebase_db.py): Firebase uygulaması zaten başlatılmış. Mevcut istemci döndürülüyor.")
        db = firestore.client()
        return db

    # 1. Yöntem: Ortam değişkeninde doğrudan JSON içeriği ara (Streamlit Secrets için)
    firebase_credentials_json_str = os.getenv("FIREBASE_CREDENTIALS") 
    
    if firebase_credentials_json_str:
        print(f"DEBUG (firebase_db.py): FIREBASE_CREDENTIALS ortam değişkeni bulundu. JSON olarak deneniyor.")
        try:
            cred_dict = json.loads(firebase_credentials_json_str)
            cred = credentials.Certificate(cred_dict) 
            firebase_admin.initialize_app(cred)
            db = firestore.client() 
            print("Firebase bağlantısı başarılı! (JSON içerik yöntemi)")
            return db
        except Exception as e:
            print(f"HATA: Firebase JSON içeriği geçersiz veya bağlantı sorunu: {e}")
            db = None
            return None
    else:
        print(f"DEBUG (firebase_db.py): FIREBASE_CREDENTIALS ortam değişkeni bulunamadı. Dosya yolu deneniyor.")
    
    # 2. Yöntem: Ortam değişkeninde JSON dosya yolu ara (Yerel .env için)
    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if firebase_credentials_path:
        print(f"DEBUG (firebase_db.py): FIREBASE_CREDENTIALS_PATH ortam değişkeni bulundu: '{firebase_credentials_path}'.")
        absolute_credentials_path = os.path.abspath(firebase_credentials_path)
        print(f"DEBUG (firebase_db.py): Aranacak mutlak yol (path): '{absolute_credentials_path}'")
        if os.path.exists(absolute_credentials_path):
            print(f"DEBUG (firebase_db.py): Dosya yolu mevcut: '{absolute_credentials_path}'.")
            try:
                cred = credentials.Certificate(absolute_credentials_path)
                firebase_admin.initialize_app(cred)
                db = firestore.client() 
                print("Firebase bağlantısı başarılı! (Dosya yolu yöntemi)")
                return db
            except Exception as e:
                print(f"HATA: Firebase bağlantısı sırasında bir sorun oluştu (dosya yolu methodu): {e}")
                db = None
                return None
        else:
            print(f"HATA: Firebase kimlik bilgileri dosyası '{absolute_credentials_path}' bulunamadı. Lütfen yolu kontrol edin.")
            db = None
            return None
    
    # Her iki yöntem de başarısız olursa
    print(f"HATA: Firebase kimlik bilgileri (.env'de FIREBASE_CREDENTIALS veya FIREBASE_CREDENTIALS_PATH) tanımlı değil. Firebase başlatılamıyor.")
    db = None
    return None

# --- CRUD Fonksiyonları (değişmedi) ---
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