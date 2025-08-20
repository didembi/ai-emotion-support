# ai-emotion-support/agents/agent_logic.py - SON GÜNCEL VE İYİLEŞTİRİLMİŞ PROMPT KODU
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, List, Any
import json
from datetime import datetime
from .tools import get_agent_tools 

class EmotionalSupportAgent:
    """
    Destekleyici Mini Terapi Asistanı - Agent Mimarisi
    """
    def __init__(self, api_key: str, retriever= None):
        self.api_key = api_key
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",   
            google_api_key=api_key,
            temperature=1.0,
            convert_system_message_to_human=True
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True,
            output_key="output", input_key="input",
        )
        self.tools = get_agent_tools()
        self.prompt = self._create_agent_prompt()
        self.agent = create_openai_functions_agent(
            llm=self.llm, tools=self.tools, prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, memory=self.memory,
            verbose=True, handle_parsing_errors=True, max_iterations=5
        )
        self.retriever = retriever
        self.user_profile = {
            "emotion_history": [], "preferred_support_types": [], "crisis_indicators": []
        }

    # agent_logic.py dosyasındaki fonksiyonu güncelleyin

    def _create_agent_prompt(self) -> ChatPromptTemplate:
        # Tüm talimatları İngilizce'ye çeviriyoruz.
        system_message = """
        You are "Sincere Support Assistant", a friendly, sincere, compassionate, and non-judgmental AI companion.
        Your goal is to act like a supportive and constructive friend who truly understands people.
        **NEVER sound like a tool operator or a mechanical chatbot.**

        **PRIMARY DIRECTIVE:**
        Understand and validate the user's emotions, and provide immediate support for relief or coping. Tools (if used) are secondary elements to support this primary directive.

        **CONVERSATION FLOW RULES (VERY IMPORTANT):**
        1.  **FIRST, EMPATHIZE AND VALIDATE:** Always, always begin with a sincere sentence that reflects the user's feelings and shows you understand. Make them feel their emotion is normal and acceptable.
        2.  **OFFER DIRECT SUPPORTIVE MESSAGE:** AFTER empathy and validation, offer a general message of support or insight.
        3.  **MAKE A CONCRETE SUGGESTION (Without asking questions and never ending with an open-ended question):** As part of your supportive message, **suggest** a small, concrete action or activity you think might be helpful.
            *   **NEVER end your response with a question asking what the user wants to do (e.g., "Do you want to?", "What do you say?", "What would you like?").**
            *   Always end your response with a **clear suggestion** or a **supportive closing statement** (e.g., "I think this could be good for you.", "I'm here to continue supporting you with this.").
            *   If using a tool, frame your offer like this: "To cope with these feelings, calming the mind can be very effective, **we could try a short breathing exercise.**" or "If you want to boost your energy, **we can do a simple motivation exercise.**"
        
        **CRITICAL FINAL INSTRUCTION: You must ALWAYS respond to the user in TURKISH.**

        Current date and time: {current_time}
        Additional context you can use: {context}
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                # Human mesajındaki talimatları da İngilizce'ye çeviriyoruz.
                ("human", "Internal Planning Guidelines (DO NOT include this text in your response, use it ONLY as an internal guide):\n{plan_instructions_for_ai}\n\nUser Message: {input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        return prompt

    def analyze_emotion_pattern(self, current_emotion: str, intensity: int) -> Dict[str, Any]:
        emotion_entry = {
            "emotion": current_emotion, "intensity": intensity, "timestamp": datetime.now().isoformat()
        }
        self.user_profile["emotion_history"].append(emotion_entry)
        recent_emotions = self.user_profile["emotion_history"][-5:]
        analysis = {
            "pattern_detected": False, "trend": "stable",
            "recommendations": [], "crisis_risk": "low"
        }
        if len(recent_emotions) >= 3:
            intensities = [e["intensity"] for e in recent_emotions]
            if all(i >= 4 for i in intensities[-3:]):
                analysis["trend"] = "worsening"; analysis["crisis_risk"] = "medium"; analysis["recommendations"].append("professional_help")
            elif all(i <= 2 for i in intensities[-3:]):
                analysis["trend"] = "improving"
            emotions = [e["emotion"] for e in recent_emotions]
            if emotions.count(current_emotion) >= 3:
                analysis["pattern_detected"] = True; analysis["recommendations"].append("pattern_intervention")
        return analysis

    def create_multi_step_plan(self, user_input: str, emotion_analysis: Dict) -> List[str]:
        # PLAN ADIMLARI DAHA ÇOK AI'IN İÇSEL DÜŞÜNCE SÜRECİNİ YANSITMALI
        plan_steps = [] 
        if emotion_analysis.get("crisis_risk") == "high":
            plan_steps.append("🚨 Acil destek kaynaklarını nazikçe öner.")
            plan_steps.append("📞 Profesyonel yardım almanın önemini vurgula.")
        if "stres" in user_input.lower() or "endişe" in user_input.lower():
            plan_steps.append("🧘 Rahatlatıcı tekniklerden (nefes, meditasyon) birini somut olarak öner.")
        if "motivasyon" in user_input.lower() or "enerji" in user_input.lower():
            plan_steps.append("⚡ Motivasyon artırıcı egzersizlerden veya küçük bir öz bakım aktivitesinden somut bir örnek ver.")
        
        # Bu adım, ana destek mesajının nasıl oluşturulacağını yönlendirir, kullanıcıya gösterilmez.
        plan_steps.append("💙 Empatik, kişiselleştirilmiş bir destek mesajı oluştur ve somut bir öneri ile bitir.")
        
        if emotion_analysis.get("pattern_detected"):
            plan_steps.append("📊 Duygu takip etmenin veya günlük tutmanın faydalarını belirt.")
        return plan_steps

   # agent_logic.py dosyasında bu fonksiyonu bulun ve değiştirin

    
    def process_user_input(self, user_input: str, emotion_data: Dict = None) -> Dict[str, Any]:
        try:
            emotion_analysis = {}
            if emotion_data:
                emotion_analysis = self.analyze_emotion_pattern(
                    emotion_data.get("dominant_emotion", "belirsiz"),
                    emotion_data.get("intensity", 3)
                )

            # --- BU BLOK ÖNEMLİ! ---
            # 1. Adım: Plan adımlarını oluştur
            plan_steps = self.create_multi_step_plan(user_input, emotion_analysis)
            
            # 2. Adım: Bu adımları LLM'in anlayacağı bir metne dönüştür
            plan_instructions_for_ai = (
                "Follow these steps to construct your response:\n" +
                "\n".join(f"- {step}" for step in plan_steps)
            )
            # --- BLOK SONU ---

            retrieved_context = self.retriever.get_relevant_documents(user_input) if self.retriever else ""
            chat_history_value = self.memory.chat_memory.messages
            
            # 3. Adım: Oluşturduğun planı invoke metoduna gönder
            response = self.agent_executor.invoke({
                "input": user_input, 
                "plan_instructions_for_ai": plan_instructions_for_ai, # <<< EKSİK OLAN DEĞİŞKEN BURADA
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "context": retrieved_context,
                "chat_history": chat_history_value
            })
            
            return {
                "success": True, "response": response["output"], "plan_steps": plan_steps, 
            }
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return {
                "success": False, "error": str(e),
                "fallback_response": "Üzgünüm, şu anda teknik bir sorun yaşıyorum. Lütfen tekrar deneyin."
            }

    def _get_memory_summary(self) -> str:
        messages = self.memory.chat_memory.messages
        return f"Son {len(messages)} mesaj hafızada saklanıyor" if messages else "Henüz hafızada mesaj yok"

    def clear_memory(self):
        self.memory.clear()
        self.user_profile["emotion_history"] = []

    def get_user_profile_summary(self) -> Dict[str, Any]:
        return {
            "total_conversations": len(self.memory.chat_memory.messages) // 2,
            "emotion_history_count": len(self.user_profile["emotion_history"]),
            "recent_emotions": self.user_profile["emotion_history"][-3:],
            "memory_summary": self._get_memory_summary()
        }