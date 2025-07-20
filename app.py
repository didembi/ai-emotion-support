import streamlit as st
import os
from dotenv import load_dotenv
from features.basic_input_response import generate_emotional_support, validate_user_input

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Emotion Support",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling and accessibility
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
        font-size: 0.9rem;
    }
    .support-message {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #333333;
    }
    
    .form-title {
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 0.8rem;
        font-size: 1rem;
    }
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        color: #333333 !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25) !important;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 0.9rem !important;
        color: #333333 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25) !important;
    }
    .stRadio > div > label {
        font-size: 0.9rem !important;
        padding: 0.4rem !important;
        color: #333333 !important;
    }
    .stCheckbox > div > label {
        font-size: 0.9rem !important;
        padding: 0.3rem !important;
        color: #333333 !important;
    }
    .stSlider > div > div > div > div {
        background-color: #1f77b4 !important;
    }
    .stButton > button {
        background-color: #1f77b4 !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    .stButton > button:hover {
        background-color: #1565c0 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    .stButton > button:disabled {
        background-color: #cccccc !important;
        color: #666666 !important;
    }
    .action-button {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.8rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin: 0.2rem !important;
    }
    .action-button:hover {
        background-color: #218838 !important;
        transform: translateY(-1px) !important;
    }
    .action-button.secondary {
        background-color: #6c757d !important;
    }
    .action-button.secondary:hover {
        background-color: #5a6268 !important;
    }
    .action-button.warning {
        background-color: #ffc107 !important;
        color: #212529 !important;
    }
    .action-button.warning:hover {
        background-color: #e0a800 !important;
    }
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    .form-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .left-column {
        flex: 1;
    }
    .right-column {
        flex: 1;
    }
    .support-container {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .subtitle {
            font-size: 0.9rem;
        }
        .form-container {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

def show_landing_page():
    """Display the welcoming landing page"""
    st.markdown('<h1 class="main-header">💙 AI Emotion Support System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Duygularınızı paylaşın, kişiselleştirilmiş destek alın</p>', unsafe_allow_html=True)
    
    # Main description
    st.markdown("""
    **Hoş geldiniz!** Bu AI arkadaşınız, sizi dinlemek, anlamak ve nazik duygusal destek sağlamak için burada. 
    Stresli, bunalmış hissediyorsanız veya sadece konuşacak birine ihtiyacınız varsa, size yardım etmek için buradayım.
    """)
    
    # Important disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Önemli:</strong> Bu AI duygusal destek sağlar ancak profesyonel ruh sağlığı bakımının yerini tutmaz. 
        Kriz durumundaysanız veya acil yardıma ihtiyacınız varsa, lütfen bir ruh sağlığı uzmanına veya kriz hattına başvurun.
    </div>
    """, unsafe_allow_html=True)

def show_sidebar_content():
    """Display sidebar content with tips, resources, and settings"""
    with st.sidebar:
        st.header("🔧 Ayarlar")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="OpenAI API anahtarınızı buraya girin veya .env dosyasında ayarlayın"
        )
        
        if not api_key:
            st.warning("⚠️ Uygulamayı kullanmak için OpenAI API anahtarınızı girin.")
            return None
        
        st.header("💡 İpuçları")
        st.markdown("""
        - **Spesifik olun**: Detay paylaşın
        - **Duygularınızı ifade edin**: Nasıl hissettiğinizi açıklayın
        - **Dürüst olun**: Samimi olun
        """)
        
        return api_key

def show_emotion_form():
    """Display comprehensive emotion input form in two columns"""
    st.subheader("🤗 Nasıl hissediyorsunuz?")
    
    # Two-column layout for form
    col1, col2 = st.columns(2)
    
    with col1:
        # Free text input
        st.markdown('<p class="form-title">📝 Duygularınızı Paylaşın</p>', unsafe_allow_html=True)
        
        user_emotion = st.text_area(
            "İçinizden geçenleri yazın...",
            height=120,
            placeholder="Bugün hiçbir şeye yetişemiyorum. Kendimi çok baskı altında hissediyorum...",
            help="Ne kadar detay verirseniz, destek o kadar kişiselleştirilmiş olur.",
            key="emotion_text"
        )
        
        # Emotion selection
        st.markdown('<p class="form-title">😊 Baskın Duygunuz</p>', unsafe_allow_html=True)
        
        emotion_options = [
            "Yalnızlık", "Stres", "Umutsuzluk", 
            "Kızgınlık", "Korku", "Motivasyon Kaybı", "Diğer"
        ]
        
        selected_emotion = st.radio(
            "Şu anda en çok hangi duyguyu hissediyorsunuz?",
            emotion_options,
            horizontal=False
        )
    
    with col2:
        # Emotion intensity
        st.markdown('<p class="form-title">📊 Duygu Şiddeti</p>', unsafe_allow_html=True)
        
        intensity = st.slider(
            "Bu duyguyu ne kadar yoğun hissediyorsunuz?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Çok hafif, 5 = Çok yoğun"
        )
        
        intensity_labels = {
            1: "Çok Hafif",
            2: "Hafif", 
            3: "Orta",
            4: "Yoğun",
            5: "Çok Yoğun"
        }
        st.caption(f"Seçilen şiddet: {intensity_labels[intensity]}")
        
        # Thought input (optional)
        st.markdown('<p class="form-title">💭 Düşünceleriniz (İsteğe Bağlı)</p>', unsafe_allow_html=True)
        
        user_thoughts = st.text_input(
            "Zihninizden geçen düşünceler:",
            placeholder="Örn: 'Yine başaramadım'",
            help="Bu alan isteğe bağlıdır."
        )
        
        # Needs selection
        st.markdown('<p class="form-title">🎯 İhtiyaçlarınız</p>', unsafe_allow_html=True)
        
        needs_options = [
            "Anlaşılmak", "Teselli", "Rahatlamak", 
            "Yalnız Olmak", "Güç Toplamak", "Destek"
        ]
        
        selected_needs = st.multiselect(
            "Şu anda neye ihtiyacınız var?",
            needs_options,
            help="Birden fazla seçebilirsiniz"
        )
    
    return {
        'emotion_text': user_emotion,
        'selected_emotion': selected_emotion,
        'intensity': intensity,
        'user_thoughts': user_thoughts,
        'selected_needs': selected_needs
    }

def show_support_generation(form_data, api_key):
    """Handle support generation with comprehensive form data"""
    if st.button("💙 Duygusal Destek Al", type="primary", disabled=not form_data['emotion_text'].strip()):
        if form_data['emotion_text'].strip():
            # Validate input
            is_valid, error_message = validate_user_input(form_data['emotion_text'])
            
            if not is_valid:
                st.error(error_message)
                return
            
            # Show loading state with encouraging message
            with st.spinner("💭 Sizi düşünüyor ve destekleyici bir yanıt hazırlıyorum..."):
                try:
                    # Create comprehensive prompt with all form data
                    comprehensive_input = create_comprehensive_prompt(form_data)
                    support_message = generate_emotional_support(comprehensive_input, api_key)
                    
                    st.session_state.support_message = support_message
                    st.session_state.form_data = form_data
                    st.success("✨ Destek mesajı oluşturuldu!")
                except Exception as e:
                    st.error(f"❌ Destek mesajı oluşturulurken hata: {str(e)}")
                    st.info("💡 Lütfen API anahtarınızı kontrol edin ve tekrar deneyin.")

def create_comprehensive_prompt(form_data):
    """Create a comprehensive prompt from all form data"""
    prompt_parts = []
    
    # Main emotion text
    prompt_parts.append(f"Ana duygu açıklaması: {form_data['emotion_text']}")
    
    # Selected emotion
    prompt_parts.append(f"Baskın duygu: {form_data['selected_emotion']}")
    
    # Intensity
    intensity_labels = {1: "çok hafif", 2: "hafif", 3: "orta", 4: "yoğun", 5: "çok yoğun"}
    prompt_parts.append(f"Duygu şiddeti: {intensity_labels[form_data['intensity']]} ({form_data['intensity']}/5)")
    
    # Thoughts (if provided)
    if form_data['user_thoughts']:
        prompt_parts.append(f"Zihinden geçen düşünceler: {form_data['user_thoughts']}")
    
    # Needs
    if form_data['selected_needs']:
        prompt_parts.append(f"İhtiyaçlar: {', '.join(form_data['selected_needs'])}")
    
    return " | ".join(prompt_parts)

def show_support_message():
    """Display the generated support message with action buttons"""
    if hasattr(st.session_state, 'support_message'):
        st.markdown('<div class="support-container">', unsafe_allow_html=True)
        st.subheader("💙 Kişiselleştirilmiş Destek Mesajınız")
        
        st.markdown(f"""
        <div class="support-message">
            {st.session_state.support_message}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons in a more compact layout
        st.subheader("🔄 Ne yapmak istiyorsunuz?")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ İyi Geldi", help="Bu mesajın size yardımcı olduğunu belirtin"):
                st.success("🎉 Harika! Size yardımcı olabildiğime sevindim.")
        
        with col2:
            if st.button("🔁 Yeniden Üret", help="Farklı bir destek mesajı oluşturun"):
                st.session_state.support_message = None
                st.rerun()
        
        with col3:
            if st.button("💾 Kaydet", help="Bu mesajı kaydedin"):
                st.info("💾 Kaydetme özelliği yakında eklenecek!")
        
        with col4:
            if st.button("📋 Günlüğe Ekle", help="Bu mesajı günlüğünüze ekleyin"):
                st.info("📋 Günlük özelliği yakında eklenecek!")
        
        # Additional options
        st.markdown("---")
        col5, col6, col7 = st.columns(3)
        
        with col5:
            if st.button("💭 Daha Fazla Paylaş"):
                st.session_state.support_message = None
                st.session_state.form_data = None
                st.rerun()
        
        with col6:
            if st.button("🆕 Yeni Başla"):
                st.session_state.support_message = None
                st.session_state.form_data = None
                st.rerun()
        
        with col7:
            if st.button("📚 Öz Bakım İpuçları"):
                show_self_care_tips()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_self_care_tips():
    """Display self-care tips and resources"""
    st.subheader("🌱 Öz Bakım İpuçları & Kaynaklar")
    
    tips = [
        "**Derin nefes alın**: 4-7-8 nefes tekniğini deneyin",
        "**Vücudunuzu hareket ettirin**: Kısa bir yürüyüş bile zihninizi temizleyebilir",
        "**Başkalarıyla bağlantı kurun**: Arkadaşlarınıza veya ailenize ulaşın",
        "**Farkındalık pratiği yapın**: Meditasyon veya topraklama egzersizleri deneyin",
        "**Yeterli uyku alın**: Dinlenme ve iyileşmeye öncelik verin",
        "**Besleyici yiyecekler yiyin**: Vücudunuzu sağlıklı seçimlerle besleyin",
        "**Ekran süresini sınırlayın**: Dijital cihazlardan ara verin",
        "**Kendinizi ifade edin**: Yazın, çizin veya bir şeyler yaratın"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")
    
    st.markdown("""
    **Unutmayın**: Öz bakım herkes için farklı görünür. Sizin için en iyi olanı bulun ve kendinize karşı sabırlı olun.
    """)

def main():
    """Main application function"""
    # Show landing page
    show_landing_page()
    
    # Get API key from sidebar
    api_key = show_sidebar_content()
    
    if not api_key:
        st.stop()
    
    # Main content area
    st.markdown("---")
    
    # Form section
    form_data = show_emotion_form()
    show_support_generation(form_data, api_key)
    
    # Support message section (appears below form)
    if hasattr(st.session_state, 'support_message'):
        show_support_message()
    else:
        st.markdown('<div class="support-container">', unsafe_allow_html=True)
        st.subheader("💭 Destek Mesajınız")
        st.info("""
        Duygularınızı paylaştıktan ve butona tıkladıktan sonra kişiselleştirilmiş duygusal destek mesajınız burada görünecek.
        
        💡 **İpucu**: Ne kadar çok paylaşırsanız, yanıt o kadar kişiselleştirilmiş ve yardımcı olur.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with additional resources
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>💙 Yalnız değilsiniz ve yardım istemek tamamen normaldir.</strong></p>
        <p>Bu AI size destek olmak için burada, ancak profesyonel yardım her zaman ihtiyacınız olduğunda mevcuttur.</p>
        <p>Unutmayın: Duygularınız geçerlidir ve destek almayı hak ediyorsunuz.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 