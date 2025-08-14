# AI Emotion Support System 💙

An AI-powered web application that provides immediate, personalized emotional support using OpenAI's GPT models. Share your feelings and receive compassionate, empathetic responses designed to help you feel heard and supported.

## 🌟 Features

- **Immediate Emotional Support**: Get personalized responses to your emotional input
- **Empathetic AI Responses**: Warm, caring, and non-judgmental support messages
- **Privacy-First Design**: No data storage, session-based interactions
- **Mobile-Friendly**: Responsive design that works on all devices
- **Accessible**: Designed with accessibility in mind
- **Professional Help Reminders**: Appropriate disclaimers and crisis resources

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation (Local)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-emotion-support
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run features/app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🌐 Deploying on Streamlit Cloud

1. Push your project to a public GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Click "New app", select your repo, set the main file path to `features/app.py`.
4. Add your environment variables (like `OPENAI_API_KEY`) in the app settings.
5. Click "Deploy" and your app will be live!

## 📖 How to Use

1. **Share Your Feelings**: Use the large text area to describe how you're feeling, what's on your mind, or any emotional challenges you're facing.
2. **Get Support**: Click "Get Emotional Support" to receive a personalized response from the AI.
3. **Read and Reflect**: The AI will provide empathetic support, coping strategies, and gentle guidance.
4. **Continue or Start Fresh**: Share more feelings or start a new session as needed.

## 🛠️ Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: AI model to use (default: gpt-3.5-turbo)

### Customization
You can customize the AI's behavior by modifying the system prompt in `features/basic_input_response.py`.

## 🔒 Privacy & Security

- **No Data Storage**: Your conversations are not stored or saved
- **Session-Based**: Each session is independent and temporary
- **Secure API Calls**: All communication with OpenAI is encrypted
- **No Tracking**: No analytics or user tracking

## ⚠️ Important Disclaimers

This AI application provides emotional support but is **not a replacement for professional mental health care**. 

- If you're experiencing a mental health crisis, please contact a professional immediately
- For crisis support, call your local Crisis hotline or emergency services
- This tool is designed for general emotional support and self-reflection

## 🏗️ Project Structure

```
ai-emotion-support/
├── agents/                        # Agent logic and Firebase integration
│   ├── __init__.py
│   ├── agent_logic.py
│   ├── firebase_db.py
│   └── tools.py
├── chroma_db/                     # Vector database files
│   ├── ...
├── data/                          # Text data for RAG
│   ├── anxiety_management.txt
│   ├── emotional_support.txt
│   ├── mindfulness_techniques.txt
│   └── stress_management.txt
├── features/
│   ├── __init__.py                # Package initialization
│   ├── app.py                     # Main Streamlit application
│   ├── basic_input_response.py    # Core AI interaction logic
│   └── requirements.txt           # Feature-specific requirements
├── rag/                           # Retrieval-Augmented Generation service
│   ├── README.md
│   └── rag_service.py
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── README.md                      # This file
├── idea.md                        # Project concept and vision
├── user-flow.md                   # Detailed user experience flow
├── tech-stack.md                  # Technology documentation
└── teck-stack.md                  # (Typo, see tech-stack.md)
```

## 🧪 Development

### Running in Development Mode
```bash
streamlit run features/app.py --server.port 8501 --server.address localhost
```

### Testing
The application includes comprehensive error handling and input validation. Test with various inputs to ensure robust behavior.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

**"Invalid OpenAI API key"**
- Verify your API key is correct
- Ensure the key has sufficient credits
- Check that the key is properly set in your `.env` file

**"Rate limit exceeded"**
- Wait a moment and try again
- Consider upgrading your OpenAI plan if this happens frequently

**Application won't start**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the correct directory
- Verify Python version is 3.8 or higher


## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

---

**Remember**: You're not alone, and it's okay to ask for help. This AI is here to support you, but professional help is always available when you need it. 💙
