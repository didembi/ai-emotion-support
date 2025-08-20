
import sys
import os
import random
from datetime import datetime

# Projenin kök dizinini sys.path'e ekler.
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(current_dir) # Bir seviye 'features'dan yukarı

if project_root not in sys.path:
    sys.path.insert(0, project_root)

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from dotenv import load_dotenv # .env dosyasını yüklemek için

# Modern UI bileşenleri için ek kütüphaneler
import json
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# firebase_db'den sadece fonksiyonları ve initialize_firebase_app'ı import ediyoruz.
from agents.firebase_db import save_conversation, load_conversations, delete_user_data, save_mood_entry, load_mood_history, firestore, initialize_firebase_app 
from agents.agent_logic import EmotionalSupportAgent 
from rag.rag_service import get_rag_retriever, reset_chroma_db


# --- Firebase Bağlantısını Başlatma ---
# Firebase uygulamasını Streamlit'in kaynak önbellekleme mekanizması ile başlat
@st.cache_resource
def setup_firebase_connection():
    """Firebase bağlantısını kurar ve Firestore istemcisini döndürür."""
    # Firebase bağlantısını başlat
    db_client = initialize_firebase_app() 
    return db_client 

# Uygulama başladığında Firebase'i başlat ve istemcisini al
firebase_db_client = setup_firebase_connection()

# Firebase istemcisinin başarılı olup olmadığını kontrol et ve session_state'e kaydet
if "db_client" not in st.session_state:
    st.session_state.db_client = firebase_db_client

if st.session_state.db_client is None:
    st.error("❌ Firebase bağlantısı kurulamadı! Lütfen .env dosyasını ve anahtar yolunu kontrol edin.")
    st.stop()


# --- AGENT BAŞLATMA (CACHE-UYUMLU) ---
# Agent'ı Firebase bağlantısı kurulduktan ve hata kontrolü yapıldıktan sonra başlatmalıyız.
@st.cache_resource
def initialize_agent():
    """Sadece agent nesnesini oluşturur ve return eder. Arayüze dokunmaz."""
    api_key = os.getenv("GOOGLE_API_KEY") 
    if not api_key: 
        return None
    try:
        # RAG retriever'ı başlat
        project_root_for_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_directory_path = os.path.join(project_root_for_app, "data")
        rag_retriever = get_rag_retriever(data_directory=data_directory_path)

        if rag_retriever is None:
            agent_instance = EmotionalSupportAgent(api_key, retriever=None)
        else:
            agent_instance = EmotionalSupportAgent(api_key, retriever=rag_retriever)
        
        return agent_instance
    except Exception as e:
        return e

# Uygulama başladığında agent'ı başlat
agent_instance = initialize_agent()
if agent_instance is None:
    st.error("⚠️ GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin."); st.stop()
elif isinstance(agent_instance, Exception):
    st.error(f"❌ Agent başlatılırken bir hata oluştu: {agent_instance}"); st.stop()


# --- SAYFA YAPILANDIRMASI VE TASARIM ---
st.set_page_config(
    page_title="AI Destek Aracı",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

duygu_listesi = ["Belirsiz", "Mutlu", "Üzgün", "Kızgın", "Endişeli", "Yorgun", "Stresli", "Heyecanlı"]
ihtiyac_listesi = ["Sadece dinlenilmek istiyorum", "Biraz motivasyona ihtiyacım var", "Stresle başa çıkmak için bir yöntem arıyorum", "Odaklanmama yardımcı ol", "Kendimi daha iyi hissetmek istiyorum"]
# Sayfa yüklendiğinde localStorage'dan tema tercihini kontrol eden JavaScript

st.markdown("""
<script>
    // Sayfa yüklendiğinde localStorage'dan tema tercihini kontrol et
    window.addEventListener('load', function() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            if (savedTheme === 'dark') {
                document.documentElement.classList.add('dark-mode-active');
            } else {
                document.documentElement.classList.remove('dark-mode-active');
            }
        }
        // Butonun simgesini ilk yüklemede doğru ayarla
        const themeButtonElement = document.querySelector('[data-testid="stButton"] button[key="theme_toggle_button"]');
        if (themeButtonElement) {
            themeButtonElement.innerText = document.documentElement.classList.contains('dark-mode-active') ? '☀️' : '🌙';
        }
    });
</script>

font_url = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
st.markdown(f'<link href="{font_url}" rel="stylesheet">', unsafe_allow_html=True)
<style>
    /* Global renk ve font değişkenleri */
    :root {
        --bg-color: #F8F9FA; /* Daha yumuşak bir arka plan */
        --text-color: #212529; /* Daha koyu, okunabilir metin */
        --accent-color: #6C63FF; /* Canlı bir vurgu rengi */
        --accent-color-light: #E0E7FF; /* Vurgu renginin açık tonu */
        --card-bg: #FFFFFF;
        --border-color: #DEE2E6; /* Hafif bir sınır rengi */
        --header-bg: linear-gradient(135deg, #6C63FF, #5158E5);
        --border-radius: 10px;
        --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --font-primary: 'Inter', sans-serif;
    }
    

    /* Streamlit'in varsayılan elementlerini gizle */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    /* Ana Uygulama Temeli */
    .stApp {
        background-color: var(--bg-color);
        font-family: var(--font-primary);
        color: var(--text-color);
    }
    
    /* ---- SLIDER DÜZELTMESİ (KARARLI YÖNTEM) ---- */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: var(--accent-color-light);
        border-radius: 5px;
        height: 8px;
    }
    div[data-testid="stSlider"] div[role="slider"] > div:last-of-type {
        background-color: var(--accent-color);
        border: 3px solid white;
        box-shadow: var(--shadow-soft);
        width: 20px;
        height: 20px;
        margin-top: -6px;
    }
    div[data-testid="stSlider"] div[role="slider"] > div:first-of-type {
        background-color: var(--accent-color);
    }
    /* ------------------------------------------- */

    /* Genel Widget Stilleri */
    .stTextArea textarea, .stSelectbox > div > div, .stTextInput input {
        border: 1px solid var(--border-color) !important;
        background-color: var(--card-bg) !important;
        border-radius: var(--border-radius) !important;
        color: var(--text-color) !important;
        box-shadow: none !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stTextArea textarea:focus, .stSelectbox > div > div:focus-within, .stTextInput input:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 2px var(--accent-color-light) !important;
    }
    
    /* Butonlar */
    .stButton > button {
        background: var(--accent-color) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-soft) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%; /* Butonu tam genişlik yap */
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover) !important;
        filter: brightness(1.1);
    }

    /* İpucu Kutusu (st.info) */
    div[data-testid="stInfo"] {
        background-color: var(--accent-color-light);
        border: none;
        border-left: 4px solid var(--accent-color);
        border-radius: var(--border-radius);
        color: var(--text-color);
    }
    div[data-testid="stInfo"] .st-emotion-cache-1xarl3l {
        color: var(--text-color); /* st.info içindeki metin rengi */
    }
    
    /* Ana Başlık (Duygularınızı Paylaşın) */
    h2 {
        font-weight: 700;
        color: var(--text-color);
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 25px;
    }

    /* Diğer Başlıklar (Nasıl Hissediyorsunuz?, Duygu Durumu vb.) */
    .st-emotion-cache-1q8dd3e {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
</style>
st.markdown(css_code, unsafe_allow_html=True)
</script>
""", unsafe_allow_html=True)


# --- YARDIMCI FONKSİYONLAR ---
# Lottie animasyonlarını yüklemek için fonksiyon
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
def show_emotion_input_form():
    st.subheader("💭 Duygularınızı Paylaşın")
    col1, col2 = st.columns([2, 1]) # Sol sütun 2 kat, sağ sütun 1 kat geniş olsun

    with col1:
        # Değişken isimlerini düzeltiyoruz
        user_input_text = st.text_area("Nasıl hissediyorsunuz?", "Bugün kendimi çok yorgun hissediyorum...", height=150, key="user_feeling_input")
        
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            selected_emotion_value = st.selectbox("Duygu Durumu", options=duygu_listesi, key="emotion_selectbox")
        with sub_col2:
            intensity_value = st.slider("Duygu Şiddeti", 1, 5, 3, key="intensity_slider")

    with col2:
        st.subheader("🎯 İhtiyaçlarınız")
        needs_value = st.selectbox(
            "Size nasıl yardımcı olabilirim?",
            options=ihtiyac_listesi,
            index=None,
            placeholder="Lütfen bir seçenek belirleyin...",
            key="needs_selectbox"
        )
        st.info("**İpucu:** Duygularınızı ve düşüncelerinizi detaylı paylaşmak, daha kişiselleştirilmiş destek almanıza yardımcı olur.")
            
    # TANIMLADIĞIMIZ DOĞRU DEĞİŞKENLERİ DÖNDÜRÜYORUZ
    return {
        "user_input": user_input_text, 
        "selected_emotion": selected_emotion_value, 
        "intensity": intensity_value, 
        "needs": needs_value
    }

def process_agent_response(agent, form_data): # Burada 'agent' parametresini kullanmaya devam ediyoruz, bu iyi
    if st.button("💙 Agent'tan Destek Al", type="primary", use_container_width=True, disabled=not form_data['user_input'].strip()):
        with st.spinner("🤖 Agent düşünüyor..."):
            response = agent.process_user_input(form_data['user_input'], emotion_data=form_data)
            if response['success']:
                st.session_state.last_response = response
                
                current_user_id = st.session_state.user_id
                
                
                # --- VERİTABANI KAYIT BAŞLANGICI ---
                conversation_entry = {
                    "user_id": current_user_id,
                    "user_message": form_data['user_input'],
                    "ai_response": response['response'],
                    "time": firestore.SERVER_TIMESTAMP 
                }
                save_success_conv = save_conversation(st.session_state.db_client, current_user_id, conversation_entry) 

                mood_entry = {
                    "user_id": current_user_id,
                    "zaman": firestore.SERVER_TIMESTAMP,
                    "duygu_siddeti": form_data['intensity'],
                    "selected_emotion": form_data['selected_emotion']
                }
                save_success_mood = save_mood_entry(st.session_state.db_client, current_user_id, mood_entry)
                # --- VERİTABANI KAYIT SONU ---

                # Streamlit session_state'e de kaydetmeye devam et (arayüzde anlık göstermek için)
                if 'history' not in st.session_state: st.session_state.history = []
                st.session_state.history.append({"user": form_data['user_input'], "ai": response['response'], "time": datetime.now()})
                
                if 'mood_history' not in st.session_state: st.session_state.mood_history = []
                st.session_state.mood_history.append({
                    "zaman": datetime.now(),
                    "duygu_siddeti": form_data['intensity'],
                    "selected_emotion": form_data['selected_emotion']
                })
                # Session state güncellendi

            else:
                st.error(response.get('fallback_response', "Bir hata oluştu."))

def show_agent_response():
    if 'last_response' in st.session_state and st.session_state.last_response:
        response = st.session_state.last_response
        st.divider()
        st.subheader("✨ Kişiselleştirilmiş Destek")
        st.markdown(response['response'])
        
        # Agent cevabına göre geri dönüş alanı
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 1, 1])
        
        with feedback_col1:
            if st.button("🔄 Tekrar Yanıt Oluştur", use_container_width=True):
                st.session_state.regenerate = True
                st.experimental_rerun()
        
        with feedback_col2:
            if st.button("✅ Tamamlandı", use_container_width=True):
                st.session_state.conversation_completed = True
                st.success("Teşekkürler! Bu konuşma tamamlandı olarak işaretlendi.")
        
        with feedback_col3:
            feedback = st.selectbox("Yanıtı Değerlendir", ["Seçiniz...", "Çok Yardımcı", "Yardımcı", "Orta", "Az Yardımcı", "Yardımcı Değil"], index=0)
            if feedback != "Seçiniz...":
                st.session_state.last_feedback = feedback
                st.success(f"Geri bildiriminiz için teşekkürler: {feedback}")
        
        # Eğer regenerate işaretlenmişse
        if 'regenerate' in st.session_state and st.session_state.regenerate:
            with st.spinner("Yeni yanıt oluşturuluyor..."):
                # Burada agent'tan yeni bir yanıt istenebilir
                # Örnek olarak aynı yanıtı tekrar gösteriyoruz
                st.session_state.regenerate = False
       
# --- ANA UYGULAMA MANTIĞI: DASHBOARD ---

# Session state'i başlat
if "last_response" not in st.session_state: st.session_state.last_response = None

if "user_id" not in st.session_state:
    st.session_state.user_id = "ai_emotion_demo_user" 
# Kullanıcı ID'si ayarlandı


# Sohbet geçmişini yükle
# Yükleme işlemleri için de st.session_state.db_client kullanılıyor
if "history_loaded" not in st.session_state: 
    loaded_conversations = load_conversations(st.session_state.db_client, st.session_state.user_id) 
    
    # YÜKLENEN GEÇMİŞİ LANGCHAIN BELLEĞİNE EKLEME (YENİ VE KRİTİK KISIM)
    if agent_instance and loaded_conversations: # agent_instance burada kullanılıyor
        # Belleği temizle (emin olmak için, eğer zaten bir şey varsa)
        agent_instance.memory.clear() 

        for entry in loaded_conversations:
            agent_instance.memory.chat_memory.add_user_message(entry['user_message'])
            agent_instance.memory.chat_memory.add_ai_message(entry['ai_response'])
    
    st.session_state.history = [
        {
            "user": entry['user_message'],
            "ai": entry['ai_response'],
            "time": entry['time'].replace(tzinfo=None) if hasattr(entry['time'], 'replace') else datetime.fromtimestamp(entry['time'].timestamp())
        }
        for entry in loaded_conversations
    ]
    st.session_state.history_loaded = True
    
# Ruh hali geçmişini yükle
if "mood_history_loaded" not in st.session_state: 
    loaded_mood_history = load_mood_history(st.session_state.db_client, st.session_state.user_id) 
    st.session_state.mood_history = [
        {
            "zaman": entry['zaman'].replace(tzinfo=None) if hasattr(entry['zaman'], 'replace') else datetime.fromtimestamp(entry['zaman'].timestamp()),
            "duygu_siddeti": entry['duygu_siddeti'],
            "selected_emotion": entry.get('selected_emotion', 'Belirsiz')
        }
        for entry in loaded_mood_history
    ]
    st.session_state.mood_history_loaded = True


# Agent'ı yükle ve hataları kontrol et (Bu blok aslında yukarıya taşındı, burada tekrar çağırmıyoruz)
# Ancak fonksiyonların argüman olarak aldığı 'agent'ı doğru şekilde iletmeliyiz.
# show_emotion_input_form() -> process_agent_response(agent_instance, form_data) olarak çağrılmalı.
# process_agent_response içindeki 'agent' parametresi 'agent_instance' olacaktır.

# Bu kısımda artık initialize_agent() çağrısı yok, o yukarıya taşındı.
# Burada sadece `process_agent_response` ve `show_agent_response` fonksiyonlarını çağıracağız.
# Bunu zaten sekmelerin içeriğinde yapıyorsunuz.
# process_agent_response(agent_instance, form_data)
# show_agent_response()

with st.sidebar:
    st.title("⚙️ Yönetim Paneli")
    st.markdown("---")
    
    # RAG Veritabanı Yönetimi
    st.subheader("📚 RAG Veritabanı")
    
    # RAG sisteminin durumunu kontrol et ve kullanıcıya bildir
    if agent_instance and agent_instance.retriever:
        st.success("RAG sistemi aktif ve hazır.")
    else:
        st.warning("RAG sistemi aktif değil. 'data' klasöründe belge olmayabilir.")

    st.markdown("Eğer `data` klasörüne yeni belgeler eklediyseniz, aşağıdaki butona tıklayarak veritabanını güncelleyebilirsiniz.")
    
    if st.button("🔄 Veritabanını Sıfırla ve Yenile"):
        with st.spinner("Veritabanı siliniyor..."):
            if reset_chroma_db():
                st.success("Veritabanı başarıyla sıfırlandı! Sayfayı yenilediğinizde veriler yeniden yüklenecektir.")
                # Sayfanın otomatik olarak yeniden çalışmasını sağlayarak veritabanının hemen oluşmasını tetikler
                st.rerun() 
            else:
                st.error("Veritabanı sıfırlanamadı veya zaten mevcut değil.")
    
    st.markdown("---")

# --- HEADER BÖLÜMÜ ---
# Header'ı tek parça olarak oluştur
st.markdown("""
<div class="dashboard-header">
    <h1 style="font-size: 1.5rem; margin: 0;">💙 Duygusal Destek Paneli</h1>
</div>
""", unsafe_allow_html=True)


# Sekmeli Navigasyon
selected_tab = option_menu(
    menu_title=None,
    options=["Konuşma Modülü", "Günlük Takip", "Analiz & Raporlar", "Kaynak & Öneriler"],
    icons=["chat-dots-heart", "journal-bookmark-fill", "graph-up-arrow", "lightbulb-fill"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "var(--accent-color-light)", "font-size": "20px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "var(--card-bg-light)", "border-bottom": "3px solid var(--accent-color-light)", "font-weight": "600"},
    }
)

# İçerik alanına padding ekleyerek header'ın altında kalmamasını sağla
st.markdown("<div class='content-card' style='margin-top: 80px;'>", unsafe_allow_html=True)

# SEKMELERİN İÇERİĞİ
if selected_tab == "Konuşma Modülü":
    # Modern başlık ve açıklama
    st.markdown("""<div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: var(--accent-color);'>💬 Agent ile Konuş</h2>
    </div>""", unsafe_allow_html=True)
    
    # İki sütunlu düzen
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; border-left: 4px solid var(--accent-color);'>
            <p>Duygularını, düşüncelerini paylaşarak anlık destek alabilirsin. Agent, verdiğin bilgilere göre sana özel yanıtlar üretecektir.</p>
        </div>""", unsafe_allow_html=True)
        
        # Detaylı Giriş Formu
        form_data = show_emotion_input_form()
        process_agent_response(agent_instance, form_data) # Burada agent_instance kullanılıyor
        show_agent_response()
    
    with col2:
        # Lottie animasyonu ekle - Psikolojiye iyi gelecek bir animasyon
        lottie_chat = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_ysrn2iwp.json") # Meditasyon/mindfulness animasyonu
        if lottie_chat:
            st_lottie(lottie_chat, height=200, key="chat_animation")
        
        # Motivasyon mesajı
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: var(--shadow-soft); border-left: 4px solid #FFD700;'>
            <h4 style='color: var(--accent-color); margin-top: 0;'>✨ Günün Mesajı</h4>
            <p style='font-style: italic;'>"Kendine nazik olmak, kendini sevmek değil, kendini iyileştirmektir."</p>
        </div>""", unsafe_allow_html=True)
        
        # İpuçları kartı
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: var(--shadow-soft);'>
            <h4 style='color: var(--accent-color); margin-top: 0;'>💡 İpuçları</h4>
            <ul style='padding-left: 20px; margin-bottom: 0;'>
                <li>Duygularınızı detaylı anlatın</li>
                <li>Spesifik durumları paylaşın</li>
                <li>İhtiyaçlarınızı belirtin</li>
            </ul>
        </div>""", unsafe_allow_html=True)

elif selected_tab == "Günlük Takip":
    # Modern başlık ve açıklama
    st.markdown("""<div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: var(--accent-color);'>📓 Günlük Kayıtların</h2>
    </div>""", unsafe_allow_html=True)
    
    # İki sütunlu düzen
    journal_col1, journal_col2 = st.columns([3, 1])
    
    with journal_col1:
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; border-left: 4px solid var(--accent-color); margin-bottom: 20px;'>
            <p>Önceki önemli konuşmaların, hedeflerin ve ruh hali kayıtların burada saklanır.</p>
        </div>""", unsafe_allow_html=True)
        
        if not st.session_state.history:
            st.markdown("""<div style='background-color: var(--card-bg); padding: 20px; border-radius: 10px; text-align: center; margin: 30px 0;'>
                <img src='https://cdn-icons-png.flaticon.com/512/6134/6134065.png' width='80'>
                <h3 style='margin-top: 15px; color: var(--accent-color);'>Henüz Kayıt Yok</h3>
                <p>Günlüğe kaydedilmiş bir konuşma bulunmuyor. 'Konuşma Modülü' üzerinden etkileşime geçebilirsiniz.</p>
            </div>""", unsafe_allow_html=True)
        else:
            # Konuşmaları en yeniden eskiye doğru göster
            for entry in reversed(st.session_state.history):
                with st.expander(f"📅 {entry['time'].strftime('%d %B %Y, %H:%M')}"):
                    st.chat_message("user", avatar="👤").write(entry['user'])
                    st.chat_message("assistant", avatar="🤖").write(entry['ai'])
    
    with journal_col2:
        # Lottie animasyonu ekle
        lottie_journal = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jl2jqcq0.json")
        if lottie_journal:
            st_lottie(lottie_journal, height=180, key="journal_animation")
        
        # İstatistik kartı
        if st.session_state.history:
            conversation_count = len(st.session_state.history)
            last_conversation = st.session_state.history[-1]['time'].strftime('%d %B')
            
            st.markdown(f"""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: var(--shadow-soft);'>
                <h4 style='color: var(--accent-color); margin-top: 0;'>📊 İstatistikler</h4>
                <p><strong>Toplam Konuşma:</strong> {conversation_count}</p>
                <p><strong>Son Konuşma:</strong> {last_conversation}</p>
            </div>""", unsafe_allow_html=True)

elif selected_tab == "Analiz & Raporlar":
    # Modern başlık ve açıklama
    st.markdown("""<div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: var(--accent-color);'>📊 Ruh Hali Analizi</h2>
    </div>""", unsafe_allow_html=True)
    
    # İki sütunlu düzen
    analysis_col1, analysis_col2 = st.columns([3, 1])
    
    with analysis_col1:
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; border-left: 4px solid var(--accent-color); margin-bottom: 20px;'>
            <p>Zaman içindeki duygu durumunuz ve şiddetinizin analizi burada görüntülenir.</p>
        </div>""", unsafe_allow_html=True)
        
        if not st.session_state.mood_history:
            st.markdown("""<div style='background-color: var(--card-bg); padding: 20px; border-radius: 10px; text-align: center; margin: 30px 0;'>
                <img src='https://cdn-icons-png.flaticon.com/512/6596/6596121.png' width='80'>
                <h3 style='margin-top: 15px; color: var(--accent-color);'>Henüz Veri Yok</h3>
                <p>Grafik oluşturmak için henüz yeterli veri yok. 'Konuşma Modülü' üzerinden etkileşime geçin.</p>
            </div>""", unsafe_allow_html=True)
        else:
            # Veri hazırlama
            df = pd.DataFrame(st.session_state.mood_history)
            df['tarih'] = pd.to_datetime(df['zaman']).dt.date
            df['selected_emotion'] = df['selected_emotion'].fillna('Belirsiz')
            daily_avg = df.groupby('tarih')['duygu_siddeti'].mean()
            
            # Kartlar içinde grafikler
            st.markdown("""<h4 style='color: var(--accent-color); margin-top: 0;'>Duygu Şiddeti Değişimi</h4>""", unsafe_allow_html=True)
            st.area_chart(daily_avg, color="#6B46C1")
            
            # Metrikler
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            with metrics_col1:
                st.metric("Ortalama Duygu Şiddeti", f"{df['duygu_siddeti'].mean():.2f} / 5")
            with metrics_col2:
                st.metric("En Yüksek Şiddet", f"{df['duygu_siddeti'].max()} / 5")
            with metrics_col3:
                st.metric("Kayıt Sayısı", f"{len(df)}")
            
            # Duygu dağılımı
            st.markdown("""<h4 style='color: var(--accent-color); margin-top: 20px;'>Duygu Dağılımı</h4>""", unsafe_allow_html=True)
            emotion_counts = df['selected_emotion'].value_counts().reset_index()
            emotion_counts.columns = ['Duygu', 'Sayı']
            st.bar_chart(emotion_counts.set_index('Duygu'), use_container_width=True, color="#764ba2")
    
    with analysis_col2:
        # Lottie animasyonu ekle
        lottie_analysis = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")
        if lottie_analysis:
            st_lottie(lottie_analysis, height=180, key="analysis_animation")
        
        # Bilgi kartı
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: var(--shadow-soft);'>
            <h4 style='color: var(--accent-color); margin-top: 0;'>💡 Analiz Bilgisi</h4>
            <p>Duygusal değişimlerinizi takip etmek, kendinizi daha iyi anlamanıza yardımcı olur.</p>
            <p>Düzenli kayıtlar, daha doğru analizler sağlar.</p>
        </div>""", unsafe_allow_html=True)
        
        # Geliştirme notu
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; border-left: 3px solid #FFD700;'>
            <p style='margin: 0; font-size: 0.9rem;'><strong>Not:</strong> Bu özellik geliştirme aşamasındadır. Yakında daha detaylı analizler eklenecektir.</p>
        </div>""", unsafe_allow_html=True)

elif selected_tab == "Kaynak & Öneriler":
    # Modern başlık ve açıklama
    st.markdown("""<div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: var(--accent-color);'>💡 Kaynaklar & Öneriler</h2>
    </div>""", unsafe_allow_html=True)
    
    # İki sütunlu düzen
    resources_col1, resources_col2 = st.columns([3, 1])
    
    with resources_col1:
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; border-left: 4px solid var(--accent-color); margin-bottom: 20px;'>
        </div>""", unsafe_allow_html=True)
        
        # Günlük hatırlatma kartı
        reminders = [
            "Bugün kendine 5 dakika ayırmayı unutma. Sadece nefes alıp ver.",
            "Mükemmel olmak zorunda değilsin. Sadece deniyor olman bile çok değerli.",
            "Küçük bir başarıyı kutla. Bir kahveyi hak ettin!",
            "Geçmişi değiştiremezsin, ama şu anki tepkini kontrol edebilirsin.",
            "Kendine karşı, en iyi arkadaşına davrandığın gibi nazik ol."
        ]
        
        st.markdown(f"""<div style='background-color: var(--card-bg); padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: var(--shadow-soft); border-left: 4px solid #FFD700;'>
            <h3 style='color: var(--accent-color); margin-top: 0;'>✨ Günün Hatırlatması</h3>
            <p style='font-size: 1.1rem; font-style: italic;'>"{random.choice(reminders)}"</p>
        </div>""", unsafe_allow_html=True)
        
        # Kaynaklar bölümü
        st.markdown("""<h3 style='color: var(--accent-color);'>📚 Faydalı Kaynaklar</h3>""", unsafe_allow_html=True)
        
        # Kaynaklar için kartlar
        resources_row1_col1, resources_row1_col2 = st.columns(2)
        with resources_row1_col1:
            st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; height: 100%; box-shadow: var(--shadow-soft);'>
                <h4 style='color: var(--accent-color); margin-top: 0;'>🧘‍♀️ Mindfulness Teknikleri</h4>
                <p>Günlük stresle başa çıkmak için mindfulness ve meditasyon teknikleri.</p>
                <button style='background-color: var(--accent-color); color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;'>Daha Fazla</button>
            </div>""", unsafe_allow_html=True)
        
        with resources_row1_col2:
            st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; height: 100%; box-shadow: var(--shadow-soft);'>
                <h4 style='color: var(--accent-color); margin-top: 0;'>😌 Stres Yönetimi</h4>
                <p>Günlük hayatta stres yönetimi için pratik ipuçları ve stratejiler.</p>
                <button style='background-color: var(--accent-color); color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;'>Daha Fazla</button>
            </div>""", unsafe_allow_html=True)
        
        resources_row2_col1, resources_row2_col2 = st.columns(2)
        with resources_row2_col1:
            st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; height: 100%; box-shadow: var(--shadow-soft);'>
                <h4 style='color: var(--accent-color); margin-top: 0;'>💪 Motivasyon Teknikleri</h4>
                <p>Motivasyonunuzu artırmak ve hedeflerinize ulaşmak için stratejiler.</p>
                <button style='background-color: var(--accent-color); color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;'>Daha Fazla</button>
            </div>""", unsafe_allow_html=True)
        
        with resources_row2_col2:
            st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; height: 100%; box-shadow: var(--shadow-soft);'>
                <h4 style='color: var(--accent-color); margin-top: 0;'>😴 Uyku Kalitesi</h4>
                <p>Daha iyi uyku için bilimsel olarak kanıtlanmış yöntemler ve öneriler.</p>
                <button style='background-color: var(--accent-color); color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;'>Daha Fazla</button>
            </div>""", unsafe_allow_html=True)
    
    with resources_col2:
        # Lottie animasyonu ekle
        lottie_resources = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jhlaooj5.json")
        if lottie_resources:
            st_lottie(lottie_resources, height=180, key="resources_animation")
        
        # Hızlı erişim kartı
        st.markdown("""<div style='background-color: var(--card-bg); padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: var(--shadow-soft);'>
            <h4 style='color: var(--accent-color); margin-top: 0;'>⚡ Hızlı Erişim</h4>
            <ul style='padding-left: 20px; margin-bottom: 0;'>
                <li>Günlük Egzersizler</li>
                <li>Nefes Teknikleri</li>
                <li>Duygu Düzenleme</li>
                <li>Pozitif Psikoloji</li>
            </ul>
        </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)