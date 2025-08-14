# ai-emotion-support/agents/firebase_db.py - SON KESİN VE NİHAİ KOD
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# DEBUG: Bu dosyanın yüklendiğini gösteren ilk mesaj
print(f"--- DEBUG (firebase_db.py): Modül yükleniyor: {__file__} ---")

# .env dosyasının tam yolunu manuel olarak belirtiyoruz.
project_root_for_db = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path_for_db = os.path.join(project_root_for_db, '.env')
load_dotenv(dotenv_path=dotenv_path_for_db) 

print(f"DEBUG (firebase_db.py): .env loaded from '{dotenv_path_for_db}'.")

# Bu modül artık global bir 'db' değişkeni TUTMAYACAK.
# initialize_firebase_app() doğrudan Firestore istemcisini döndürecek.
# Diğer fonksiyonlar (save, load vb.) artık 'db' argümanı alacak.

def initialize_firebase_app():
    """Firebase Admin SDK'yı başlatır ve Firestore istemcisini döndürür."""
    print(f"DEBUG (firebase_db.py): initialize_firebase_app fonksiyonu çağrıldı.")

    if firebase_admin._apps:
        # Eğer uygulama zaten başlatılmışsa, mevcut Firestore istemcisini döndür.
        print("DEBUG (firebase_db.py): Firebase uygulaması zaten başlatılmış. Mevcut istemci döndürülüyor.")
        return firestore.client()

    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

    print(f"DEBUG (firebase_db.py): FIREBASE_CREDENTIALS_PATH from .env: '{firebase_credentials_path}'")
    if not firebase_credentials_path:
        print(f"DEBUG (firebase_db.py): FIREBASE_CREDENTIALS_PATH hala .env'de tanımlı değil. (initialize_firebase_app)")
        return None # Hata durumunda None döndür

    absolute_credentials_path = os.path.abspath(firebase_credentials_path)
    print(f"DEBUG (firebase_db.py): Aranacak mutlak yol: '{absolute_credentials_path}'")

    if os.path.exists(absolute_credentials_path):
        try:
            cred = credentials.Certificate(absolute_credentials_path)
            firebase_admin.initialize_app(cred)
            db_client = firestore.client() # db istemcisi burada oluşturuldu
            print("Firebase bağlantısı başarılı! (firebase_db.py)")
            return db_client # BAŞARILI DURUMDA db istemcisini DÖNDÜR
        except Exception as e:
            print(f"Firebase bağlantısı hatası (firebase_db.py - initialize_app): {e}")
            return None # Hata durumunda None döndür
    else:
        print(f"Firebase kimlik bilgileri dosyası '{absolute_credentials_path}' bulunamadı. (firebase_db.py - initialize_app)")
        return None # Dosya bulunamazsa None döndür


# --- CRUD Fonksiyonları ---
# Bu fonksiyonlar artık 'db' argümanı alacak.
def save_conversation(db_client, user_id: str, conversation_entry: dict): # db_client argümanı eklendi
    if db_client: # db_client None değilse devam et
        try:
            print(f"DEBUG (firebase_db.py): Konuşma kaydetme denemesi: User '{user_id}'")
            doc_ref = db_client.collection('users').document(user_id).collection('conversations').document()
            doc_ref.set(conversation_entry)
            print(f"DEBUG (firebase_db.py): Konuşma başarıyla kaydedildi: ID '{doc_ref.id}'")
            return True
        except Exception as e:
            print(f"DEBUG (firebase_db.py): Konuşma kaydetme hatası: {e}")
            return False
    print(f"DEBUG (firebase_db.py): db istemcisi başlatılmadığı için konuşma kaydedilemedi.")
    return False

def load_conversations(db_client, user_id: str) -> list: # db_client argümanı eklendi
    conversations = []
    if db_client: # db_client None değilse devam et
        try:
            print(f"DEBUG (firebase_db.py): Konuşma yükleme denemesi: User '{user_id}'")
            docs = db_client.collection('users').document(user_id).collection('conversations').order_by('time', direction=firestore.Query.ASCENDING).stream()
            for doc in docs:
                entry = doc.to_dict()
                conversations.append(entry)
            print(f"DEBUG (firebase_db.py): {user_id} için {len(conversations)} konuşma yüklendi.")
        except Exception as e:
            print(f"DEBUG (firebase_db.py): Konuşma yükleme hatası: {e}")
    else:
        print(f"DEBUG (firebase_db.py): db istemcisi başlatılmadığı için konuşmalar yüklenemedi.")
    return conversations

def delete_user_data(db_client, user_id: str): # db_client argümanı eklendi
    if db_client: # db_client None değilse devam et
        try:
            print(f"DEBUG (firebase_db.py): Kullanıcı verisi silme denemesi: User '{user_id}'")
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
            print(f"DEBUG (firebase_db.py): Kullanıcı {user_id} verileri başarıyla silindi.")
            return True
        except Exception as e:
            print(f"DEBUG (firebase_db.py): Kullanıcı verisi silme hatası: {e}")
            return False
    print(f"DEBUG (firebase_db.py): db istemcisi başlatılmadığı için kullanıcı verisi silinemedi.")
    return False

def save_mood_entry(db_client, user_id: str, mood_entry: dict): # db_client argümanı eklendi
    if db_client: # db_client None değilse devam et
        try:
            print(f"DEBUG (firebase_db.py): Ruh hali kaydetme denemesi: User '{user_id}'")
            doc_ref = db_client.collection('users').document(user_id).collection('mood_history').document()
            doc_ref.set(mood_entry)
            print(f"DEBUG (firebase_db.py): Ruh hali başarıyla kaydedildi.")
            return True
        except Exception as e:
            print(f"DEBUG (firebase_db.py): Ruh hali kaydetme hatası: {e}")
            return False
    print(f"DEBUG (firebase_db.py): db istemcisi başlatılmadığı için ruh hali kaydedilemedi.")
    return False

def load_mood_history(db_client, user_id: str) -> list: # db_client argümanı eklendi
    mood_history = []
    if db_client: # db_client None değilse devam et
        try:
            print(f"DEBUG (firebase_db.py): Ruh hali yükleme denemesi: User '{user_id}'")
            docs = db_client.collection('users').document(user_id).collection('mood_history').order_by('zaman', direction=firestore.Query.ASCENDING).stream()
            for doc in docs:
                entry = doc.to_dict()
                mood_history.append(entry)
            print(f"DEBUG (firebase_db.py): {user_id} için {len(mood_history)} ruh hali kaydı yüklendi.")
        except Exception as e:
            print(f"DEBUG (firebase_db.py): Ruh hali geçmişi yükleme hatası: {e}")
    else:
        print(f"DEBUG (firebase_db.py): db istemcisi başlatılmadığı için ruh hali geçmişi yüklenemedi.")
    return mood_history