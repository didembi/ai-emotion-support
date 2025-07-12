import streamlit as st
import os
from dotenv import load_dotenv
from features.basic_input_response import generate_emotional_support

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Emotion Support",
    page_icon="💙",
    layout="wide"
)

def main():
    st.title("💙 AI Emotion Support System")
    st.markdown("Share your feelings and receive personalized emotional support from AI.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key here or set it in .env file"
        )
        
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key to use the app.")
            st.stop()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("How are you feeling?")
        user_emotion = st.text_area(
            "Share your emotions, thoughts, or what's on your mind...",
            height=200,
            placeholder="I'm feeling overwhelmed with work lately...",
            help="Be as detailed as you'd like. The more context you provide, the better the AI can support you."
        )
        
        if st.button("Get Emotional Support", type="primary", disabled=not user_emotion.strip()):
            if user_emotion.strip():
                with st.spinner("Generating personalized support message..."):
                    try:
                        support_message = generate_emotional_support(user_emotion, api_key)
                        st.session_state.support_message = support_message
                    except Exception as e:
                        st.error(f"Error generating support message: {str(e)}")
    
    with col2:
        st.subheader("AI Support Message")
        if hasattr(st.session_state, 'support_message'):
            st.markdown(st.session_state.support_message)
        else:
            st.info("💭 Your personalized emotional support message will appear here after you share your feelings and click the button.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>💙 This AI is here to provide emotional support, but it's not a replacement for professional mental health care.</p>
            <p>If you're in crisis, please reach out to a mental health professional or crisis hotline.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 