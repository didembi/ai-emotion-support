import streamlit as st
import os
from dotenv import load_dotenv
from agent_logic import EmotionalSupportAgent
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Emotion Support Agent",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .agent-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-feature {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .memory-box {
        background-color: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .plan-step {
        background-color: #fff3e0;
        border-left: 3px solid #ff9800;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 3px;
    }
    .tool-used {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

def initialize_agent():
    """Agent'ı başlatır"""
    if 'agent' not in st.session_state:
        api_key = st.sidebar.text_input(
            "🔑 OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="OpenAI API anahtarınızı girin"
        )
        
        if api_key:
            try:
                st.session_state.agent = EmotionalSupportAgent(api_key)
                st.sidebar.success("✅ Agent başarıyla başlatıldı!")
                return True
            except Exception as e:
                st.sidebar.error(f"❌ Agent başlatılamadı: {str(e)}")
                return False
        else:
            st.sidebar.warning("⚠️ API anahtarı gerekli")
            return False
    return True

def show_agent_header():
    """Agent başlığını gösterir"""
    st.markdown("""
    <div class="agent-header">
        <h1> Destekleyici Mini Terapi Asistanı</h1>
        <p>Hafıza, Araç Kullanımı ve Çok Adımlı Planlama ile Güçlendirilmiş AI Agent</p>
    </div>
    """, unsafe_allow_html=True)

def show_agent_features():
    """Agent özelliklerini gösterir"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-feature">
            <h3>🧠 Hafıza</h3>
            <p>Önceki konuşmalarınızı hatırlar ve kişiselleştirilmiş destek sağlar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-feature">
            <h3>🛠️ Araç Kullanımı</h3>
            <p>Meditasyon, egzersiz ve kaynak önerileri için özel araçlar kullanır</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-feature">
            <h3>📋 Çok Adımlı Planlama</h3>
            <p>Karmaşık durumlar için adım adım çözüm planları oluşturur</p>
        </div>
        """, unsafe_allow_html=True)

def show_sidebar_info():
    """Sidebar bilgilerini gösterir"""
    with st.sidebar:
        st.header("📊 Agent Durumu")
        
        if 'agent' in st.session_state:
            profile = st.session_state.agent.get_user_profile_summary()
            
            st.markdown("""
            <div class="memory-box">
                <h4>🧠 Hafıza Durumu</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric("Toplam Konuşma", profile['total_conversations'])
            st.metric("Duygu Geçmişi", profile['emotion_history_count'])
            
            if profile['recent_emotions']:
                st.subheader("📈 Son Duygular")
                for emotion in profile['recent_emotions']:
                    st.write(f"• {emotion['emotion']} ({emotion['intensity']}/5)")
            
            st.info(profile['memory_summary'])
            
            if st.button("🗑️ Hafızayı Temizle"):
                st.session_state.agent.clear_memory()
                st.success("Hafıza temizlendi!")
                st.rerun()
        
        st.header("ℹ️ Kullanım İpuçları")
        st.markdown("""
        - **Detaylı olun**: Ne hissettiğinizi açık bir şekilde ifade edin
        - **Dürüst olun**: Agent size daha iyi yardım edebilir
        - **Sabırlı olun**: Agent düşünme süreci biraz zaman alabilir
        - **Araçları deneyin**: Önerilen egzersizleri ve teknikleri uygulayın
        """)

def show_emotion_input_form():
    """Duygu girişi formunu gösterir"""
    st.subheader("💭 Duygularınızı Paylaşın")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_area(
            "Nasıl hissediyorsunuz? Ne düşünüyorsunuz?",
            height=150,
            placeholder="Bugün kendimi çok yorgun hissediyorum. İş stresi beni çok etkiliyor ve hiçbir şeye motivasyonum yok...",
            key="user_emotion_input"
        )
    
    with col2:
        st.subheader("🎯 Ek Bilgiler")
        
        selected_emotion = st.selectbox(
            "Baskın duygunuz:",
            ["Belirsiz", "Stres", "Endişe", "Üzüntü", "Kızgınlık", "Yorgunluk", "Yalnızlık", "Motivasyon Kaybı"]
        )
        
        intensity = st.slider(
            "Duygu şiddeti (1-5):",
            min_value=1,
            max_value=5,
            value=3
        )
        
        needs = st.multiselect(
            "İhtiyaçlarınız:",
            ["Anlaşılmak", "Teselli", "Pratik Çözüm", "Rahatlamak", "Motivasyon", "Profesyonel Yönlendirme"]
        )
    
    return {
        "user_input": user_input,
        "selected_emotion": selected_emotion,
        "intensity": intensity,
        "needs": needs
    }

def process_agent_response(form_data):
    """Agent yanıtını işler ve gösterir"""
    if st.button("💙 Agent'tan Destek Al", type="primary", disabled=not form_data['user_input'].strip()):
        if form_data['user_input'].strip():
            with st.spinner("🤖 Agent düşünüyor ve plan yapıyor..."):
                try:
                    # Emotion data hazırla
                    emotion_data = {
                        "selected_emotion": form_data['selected_emotion'],
                        "intensity": form_data['intensity'],
                        "needs": form_data['needs']
                    }
                    
                    # Agent'ı çalıştır
                    response = st.session_state.agent.process_user_input(
                        form_data['user_input'],
                        emotion_data
                    )
                    
                    if response['success']:
                        st.session_state.last_response = response
                        st.success("✅ Agent yanıtı hazır!")
                    else:
                        st.error(f"❌ Hata: {response['error']}")
                        if 'fallback_response' in response:
                            st.info(response['fallback_response'])
                
                except Exception as e:
                    st.error(f"❌ Beklenmeyen hata: {str(e)}")

def show_agent_response():
    """Agent yanıtını gösterir"""
    if 'last_response' in st.session_state:
        response = st.session_state.last_response
        
        st.subheader("🤖 Agent Yanıtı")
        
        # Plan adımlarını göster
        if response.get('plan_steps'):
            st.subheader("📋 Çalışma Planı")
            for i, step in enumerate(response['plan_steps'], 1):
                st.markdown(f"""
                <div class="plan-step">
                    <strong>{i}.</strong> {step}
                </div>
                """, unsafe_allow_html=True)
        
        # Ana yanıtı göster
        st.subheader("💙 Kişiselleştirilmiş Destek")
        st.markdown(f"""
        <div style="background-color: #f0f8ff; border-left: 4px solid #4169e1; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            {response['response']}
        </div>
        """, unsafe_allow_html=True)
        
        # Kullanılan araçları göster
        if response.get('tools_used'):
            st.subheader("🛠️ Kullanılan Araçlar")
            for tool in response['tools_used']:
                st.markdown(f'<span class="tool-used">🔧 {tool}</span>', unsafe_allow_html=True)
        
        # Duygu analizi göster
        if response.get('emotion_analysis'):
            analysis = response['emotion_analysis']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Duygu Trendi", analysis.get('trend', 'stable'))
            
            with col2:
                st.metric("Kriz Riski", analysis.get('crisis_risk', 'low'))
            
            with col3:
                pattern = "Evet" if analysis.get('pattern_detected') else "Hayır"
                st.metric("Desen Tespit", pattern)
        
        # Aksiyon butonları
        st.subheader("🎯 Ne Yapmak İstiyorsunuz?")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Yardımcı Oldu"):
                st.success("🎉 Harika! Size yardımcı olabildiğime sevindim.")
        
        with col2:
            if st.button("🔄 Yeni Yanıt"):
                # Aynı girdi ile yeni yanıt al
                st.info("🔄 Yeni yanıt için tekrar 'Agent'tan Destek Al' butonuna tıklayın.")
        
        with col3:
            if st.button("💾 Kaydet"):
                # Yanıtı kaydetme özelliği
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                saved_response = {
                    "timestamp": timestamp,
                    "response": response['response'],
                    "emotion_analysis": response.get('emotion_analysis', {})
                }
                
                if 'saved_responses' not in st.session_state:
                    st.session_state.saved_responses = []
                
                st.session_state.saved_responses.append(saved_response)
                st.success("💾 Yanıt kaydedildi!")
        
        with col4:
            if st.button("🆕 Yeni Konuşma"):
                if 'last_response' in st.session_state:
                    del st.session_state.last_response
                st.rerun()

def show_saved_responses():
    """Kaydedilen yanıtları gösterir"""
    if 'saved_responses' in st.session_state and st.session_state.saved_responses:
        st.subheader("💾 Kaydedilen Yanıtlar")
        
        for i, saved in enumerate(reversed(st.session_state.saved_responses)):
            with st.expander(f"📅 {saved['timestamp']}"):
                st.markdown(saved['response'])
                
                if saved.get('emotion_analysis'):
                    st.json(saved['emotion_analysis'])

def main():
    """Ana uygulama fonksiyonu"""
    show_agent_header()
    
    # Agent'ı başlat
    if not initialize_agent():
        st.stop()
    
    show_agent_features()
    show_sidebar_info()
    
    # Ana içerik
    st.markdown("---")
    
    # Form ve yanıt bölümü
    form_data = show_emotion_input_form()
    process_agent_response(form_data)
    
    # Agent yanıtını göster
    show_agent_response()
    
    # Kaydedilen yanıtlar
    st.markdown("---")
    show_saved_responses()
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0; margin-top: 3rem; border-top: 1px solid #eee;'>
        <p><strong>🤖 Bu bir AI Agent sistemidir</strong></p>
        <p>Hafıza, araç kullanımı ve çok adımlı planlama yetenekleri ile donatılmıştır.</p>
        <p>Profesyonel yardımın yerini tutmaz, ancak anlık duygusal destek sağlar.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()