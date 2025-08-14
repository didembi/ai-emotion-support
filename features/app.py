# ai-emotion-support/features/app.py - SON VE KESİN KOD (TÜM İYİLEŞTİRMELER DAHİL)
# --- Gerekli importlar ve proje yolu tanımlama ---
import sys
import os
import random
from datetime import datetime
import json
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components


# Projenin kök dizinini sys.path'e ekler.
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(current_dir) 

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from dotenv import load_dotenv 

# Firebase ve Agent/RAG modüllerini import ediyoruz.
from agents.firebase_db import save_conversation, load_conversations, delete_user_data, save_mood_entry, load_mood_history, firestore, initialize_firebase_app 
from agents.agent_logic import EmotionalSupportAgent 
from rag.rag_service import get_rag_retriever 


# Ortam değişkenlerini yükle
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path) 


# --- LOTTIE ANIMASYON YÜKLEYİCİ ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# --- Firebase Bağlantısını Başlatma ---
@st.cache_resource
def get_firebase_db_client():
    return initialize_firebase_app() 

firebase_db_client_instance = get_firebase_db_client()

if firebase_db_client_instance is None:
    st.error("❌ Firebase bağlantısı kurulamadı! Lütfen .env dosyanızı ve anahtar yolunuzu kontrol edin.")
    st.stop()


# --- AGENT BAŞLATMA (CACHE-UYUMLU) ---
@st.cache_resource
def initialize_agent():
    api_key = os.getenv("GOOGLE_API_KEY") 
    if not api_key: 
        return None
    try:
        project_root_for_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_directory_path = os.path.join(project_root_for_app, "data")
        rag_retriever = get_rag_retriever(data_directory=data_directory_path)

        if rag_retriever is None:
            agent_instance = EmotionalSupportAgent(api_key, retriever=None) 
        else:
            agent_instance = EmotionalSupportAgent(api_key, retriever=rag_retriever) 
        
        return agent_instance
    except Exception as e:
        st.exception(e) # Streamlit'te hatayı göster
        return None

agent_instance = initialize_agent() 
if agent_instance is None:
    st.error("⚠️ Agent başlatılırken bir sorun oluştu veya GOOGLE_API_KEY bulunamadı. Lütfen kontrol edin."); st.stop()


# --- SAYFA YAPILANDIRMASI VE TASARIM ---
st.set_page_config(
    page_title="AI Destek Aracı",
    page_icon="💙", # Sayfa ikonunu daha genel bir emojiye çevirdim
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TEMA YÖNETİMİ ---
if 'is_dark_mode' not in st.session_state:
    st.session_state.is_dark_mode = False 

def toggle_theme_mode():
    st.session_state.is_dark_mode = not st.session_state.is_dark_mode

# JavaScript ile localStorage'dan tema tercihini okuyup uygulamak
# Bu JS kodu, Streamlit tarafından render edilen HTML'e eklenir.
components.html("""
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
        // QuerySelector ile elementi bul, çünkü Streamlit'in iç yapısı değişebilir.
        const themeButtonElement = document.querySelector('[data-testid="stButton"] button[key="theme_toggle_button"]');
        if (themeButtonElement) {
            themeButtonElement.innerText = document.documentElement.classList.contains('dark-mode-active') ? '☀️' : '🌙';
        }
    });
    
    // Tema değişikliğini izle ve localStorage'a kaydet, buton simgesini güncelle
    // MutationObserver, DOM'daki sınıf değişikliklerini yakalar.
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const isDarkMode = document.documentElement.classList.contains('dark-mode-active');
                localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
                
                const themeButtonElement = document.querySelector('[data-testid="stButton"] button[key="theme_toggle_button"]');
                if (themeButtonElement) {
                    themeButtonElement.innerText = isDarkMode ? '☀️' : '🌙';
                }
            }
        });
    });
    observer.observe(document.documentElement, { attributes: true });
</script>
""", height=0, width=0)

# --- MODERN CSS ---
# CSS değişkenleri ve stiller burada tanımlanır.
st.markdown("""
<style>
    /* Global renk ve font değişkenleri - Tek bir yerde tanımlama */
    :root {
        /* Temel Değişkenler - Açık Tema */
        --bg-color-light: #F7F9FC;
        --text-color-light: #1A1A1A;
        --accent-color-light: #5B5FE0;
        --user-bubble-bg-light: #E8ECF3;
        --card-bg-light: #FFFFFF;
        --header-bg-light: linear-gradient(135deg, #5B5FE0, #7F4CD9);
        
        /* Temel Değişkenler - Koyu Tema */
        --bg-color-dark: #121421;
        --text-color-dark: #EAEAEA;
        --accent-color-dark: #A08CFF;
        --user-bubble-bg-dark: #2C2F3A;
        --card-bg-dark: #1E2130;
        --header-bg-dark: linear-gradient(135deg, #7F4CD9, #5B5FE0);
        
        /* Aktif Tema Değişkenleri - Varsayılan olarak açık tema */
        --bg-color: var(--bg-color-light);
        --text-color: var(--text-color-light);
        --accent-color: var(--accent-color-light);
        --user-bubble-bg: var(--user-bubble-bg-light);
        --card-bg: var(--card-bg-light);
        --header-bg: var(--header-bg-light);
        
        /* Diğer Değişkenler */
        --border-radius: 12px;
        --shadow-soft: 0 4px 15px rgba(0,0,0,0.1);
        --shadow-hover: 0 8px 20px rgba(0,0,0,0.15);
        --font-primary: 'Inter', sans-serif;
    }
    
    /* Tema Geçişleri için Global Animasyon */
    * {
        transition: background-color 0.3s, color 0.3s, border-color 0.3s, box-shadow 0.3s;
    }

    /* Streamlit'in varsayılan elementlerini gizle */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    /* Ana Uygulama Temeli */
    .stApp {
        background-color: var(--bg-color);
        font-family: var(--font-primary);
        color: var(--text-color);
        padding-top: 0 !important;
    }
    .st-emotion-cache-z5fcl4 { /* Streamlit'in ana içerik container'ı */
        padding-top: 0 !important;
    }
    
    /* Koyu Tema Aktif Olduğunda */
    .dark-mode-active { /* html elementine eklenen sınıf */
        --bg-color: var(--bg-color-dark);
        --text-color: var(--text-color-dark);
        --accent-color: var(--accent-color-dark);
        --user-bubble-bg: var(--user-bubble-bg-dark);
        --card-bg: var(--card-bg-dark);
        --header-bg: var(--header-bg-dark);
    }
    
    /* Dashboard Header */
    .dashboard-header {
        background: var(--header-bg);
        padding: 1.5rem; 
        border-radius: 0;
        color: white;
        margin-bottom: 2rem; 
        box-shadow: var(--shadow-soft);
        text-align: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .dashboard-header h1 {
        font-size: 2.5rem; 
        font-weight: 700; 
        margin: 0;
        display: inline-flex;
        align-items: center; 
        gap: 1rem;
        color: white;
    }
    
    .dashboard-header p { 
        font-size: 1.1rem; 
        opacity: 0.9; 
        margin-top: 0.5rem; 
        color: white; 
    }
    
    /* İçerik Kartları */
    .content-card {
        background-color: var(--card-bg); 
        padding: 2rem; 
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft); 
        border: 1px solid rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    /* Seçili kartlar için stil */
    .content-card:hover {
        box-shadow: var(--shadow-hover);
        border-left: 4px solid var(--accent-color);
    }
    
    /* iframe için stil düzeltmeleri */
    iframe {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-radius: var(--border-radius) !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }
    
    /* Input ve Widget'lar - Tema değişkenlerini kullanarak otomatik eşleştirme */
    .stSelectbox>div>div, 
    .stSlider>div>div>div,
    .stTextArea>div>div>textarea,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input { 
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: rgba(0,0,0,0.1) !important;
    }
    
    .stSlider > div > div > div { 
        background: var(--accent-color) !important; 
    }

    /* Sekme Navigasyonu */
    div.st-emotion-cache-1g8w9ub {
        padding: 0 !important;
        background-color: transparent !important;
        margin-top: 80px;
        border-radius: 0;
    }
    
    .st-emotion-cache-11r0f6z {
        color: var(--text-color) !important;
        font-size: 16px !important;
        text-align: center !important;
        margin: 0px !important;
        background-color: var(--card-bg) !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.3s ease !important;
        padding: 1rem 1.5rem !important;
    }
    
    .st-emotion-cache-10mte23 {
        border-bottom: 3px solid var(--accent-color) !important;
        background-color: var(--card-bg) !important;
        color: var(--accent-color) !important;
        font-weight: 600 !important;
    }

    /* Chat Mesajları */
    [data-testid="stChatMessageContent"] {
        border-radius: 18px; 
        border: none; 
        padding: 1rem 1.5rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
    }
    
    [data-testid="stChatMessageContent"] p { 
        font-size: 1rem; 
        line-height: 1.6;
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-user"]) [data-testid="stChatMessageContent"] { 
        background-color: var(--user-bubble-bg); 
        color: var(--text-color);
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] { 
        background: var(--accent-color); 
        color: white; 
    }

    /* Butonlar */
    .stButton > button {
        background: var(--accent-color) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-soft) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover) !important;
        opacity: 0.9;
    }
    
    /* Tema Değiştirme Butonu */
    [key="theme_toggle_button"] {
        background: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-soft) !important;
    }
    
    [key="theme_toggle_button"]:hover {
        transform: scale(1.05) !important;
        box-shadow: var(--shadow-hover) !important;
    }
    
    /* Ek bilgi kutusu */
    .info-box {
        background-color: var(--card-bg);
        padding: 15px;
        border-radius: var(--border-radius);
        border-left: 5px solid var(--accent-color);
        box-shadow: var(--shadow-soft);
        margin-top: 15px;
        font-size: 0.95rem;
        line-height: 1.5;
        color: var(--text-color);
    }
    .info-box strong {
        color: var(--accent-color);
    }

    /* Sabit header altındaki boşluk */
    div[data-testid="stVerticalBlock"] {
        padding-top: 80px;
    }

    /* Genel input alanlarının border radius'unu uyumlu hale getirme */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: var(--border-radius);
    }

</style>

<!-- Streamlit'te çalışacak şekilde JavaScript kodu -->  
<script>
    window.addEventListener('load', function() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            if (savedTheme === 'dark') {
                document.documentElement.classList.add('dark-mode-active');
            } else {
                document.documentElement.classList.remove('dark-mode-active');
            }
        }
        const themeButtonElement = document.querySelector('[data-testid="stButton"] button[key="theme_toggle_button"]');
        if (themeButtonElement) {
            themeButtonElement.innerText = document.documentElement.classList.contains('dark-mode-active') ? '☀️' : '🌙';
        }
    });
    
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const isDarkMode = document.documentElement.classList.contains('dark-mode-active');
                localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
                
                const themeButtonElement = document.querySelector('[data-testid="stButton"] button[key="theme_toggle_button"]');
                if (themeButtonElement) {
                    themeButtonElement.innerText = isDarkMode ? '☀️' : '🌙';
                }
            }
        });
    });
    observer.observe(document.documentElement, { attributes: true });
</script>
""", unsafe_allow_html=True)


# --- HEADER BÖLÜMÜ ---
st.markdown("""
<div class="dashboard-header">
    <h1 style="font-size: 1.5rem; margin: 0;">🚀 Duygusal Sağlık Paneli</h1>
    <div id="theme-toggle-container"></div>
</div>
""", unsafe_allow_html=True)

theme_button_placeholder = st.empty()
theme_button = theme_button_placeholder.button(
    "🌙" if not st.session_state.is_dark_mode else "☀️", 
    key="theme_toggle_button", 
    on_click=toggle_theme_mode,
    help="Tema değiştir (Açık/Koyu)"
)

st.markdown("""
<script>
    const themeToggleContainer = document.getElementById('theme-toggle-container');
    const themeButtonElement = document.querySelector('[data-testid="stButton"] button[key="theme_toggle_button"]');
    
    if (themeToggleContainer && themeButtonElement && !themeToggleContainer.contains(themeButtonElement.closest('[data-testid="stButton"]'))) {
        themeToggleContainer.appendChild(themeButtonElement.closest('[data-testid="stButton"]'));
    }
</script>
""", unsafe_allow_html=True)


# Sekmeli Navigasyon
selected_tab = option_menu(
    menu_title=None,
    options=["Konuşma Modülü", "Günlük Takip", "Analiz & Raporlar", "Kaynak & Öneriler"],
    icons=["chat-dots-heart", "journal-bookmark-fill", "graph-up-arrow", "lightbulb-fill"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "var(--accent-color)", "font-size": "20px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "var(--card-bg)", "border-bottom": "3px solid var(--accent-color)", "font-weight": "600", "color": "var(--text-color)"},
    }
)

st.markdown("<div class='content-card' style='padding-top: 20px;'>", unsafe_allow_html=True)


# SEKMELERİN İÇERİĞİ
if selected_tab == "Konuşma Modülü":
    st.header("💬 Agent ile Konuş")
    st.markdown("Duygularını, düşüncelerini paylaşarak anlık destek alabilirsin. Agent, verdiğin bilgilere göre sana özel yanıtlar üretecektir.")
    
    form_data = show_emotion_input_form()
    process_agent_response(agent_instance, form_data)
    show_agent_response()

elif selected_tab == "Günlük Takip":
    st.header("📓 Günlük Kayıtların")
    st.markdown("Önceki önemli konuşmaların, hedeflerin ve ruh hali kayıtların burada saklanır.")
    if not st.session_state.history:
        st.info("Henüz günlüğe kaydedilmiş bir konuşma yok.")
    else:
        for entry in reversed(st.session_state.history):
            with st.expander(f"📅 {entry['time'].strftime('%d %B %Y, %H:%M')}"):
                st.chat_message("user", avatar="👤").write(entry['user'])
                st.chat_message("assistant", avatar="🤖").write(entry['ai'])

elif selected_tab == "Analiz & Raporlar":
    st.header("📊 Ruh Hali Analizi")
    if not st.session_state.mood_history:
        st.info("Grafik oluşturmak için henüz yeterli veri yok. 'Konuşma Modülü' üzerinden etkileşime geçin.")
    else:
        st.markdown("Zaman içindeki duygu şiddeti değişimin:")
        df = pd.DataFrame(st.session_state.mood_history)
        df['tarih'] = pd.to_datetime(df['zaman']).dt.date
        
        df['selected_emotion'] = df['selected_emotion'].fillna('Belirsiz') 
        
        daily_avg = df.groupby('tarih')['duygu_siddeti'].mean()
        
        st.area_chart(daily_avg, color="#6B46C1") 
        
        st.metric("Ortalama Duygu Şiddeti", f"{df['duygu_siddeti'].mean():.2f} / 5")
        
        st.subheader("Duygu Dağılımı")
        emotion_counts = df['selected_emotion'].value_counts().reset_index()
        emotion_counts.columns = ['Duygu', 'Sayı']
        st.bar_chart(emotion_counts.set_index('Duygu'), use_container_width=True, color="#764ba2")

        st.warning("Bu özellik geliştirme aşamasındadır.")

elif selected_tab == "Kaynak & Öneriler":
    st.header("💡 Günlük Tavsiyeler & Hatırlatmalar")
    st.markdown("Her gün kendine bir iyilik yap.")
    reminders = [
        "Bugün kendine 5 dakika ayırmayı unutma. Sadece nefes alıp ver.",
        "Mükemmel olmak zorunda değilsin. Sadece deniyor olman bile çok değerli.",
        "Küçük bir başarıyı kutla. Bir kahveyi hak ettin!",
        "Geçmişi değiştiremezsin, ama şu anki tepkini kontrol edebilirsin.",
        "Kendine karşı, en iyi arkadaşına davrandığın gibi nazik ol."
    ]
    st.info(f"**Bugünün Hatırlatması:** {random.choice(reminders)}")

st.markdown("</div>", unsafe_allow_html=True)