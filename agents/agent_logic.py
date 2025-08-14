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

    def _create_agent_prompt(self) -> ChatPromptTemplate:
        system_message = """
        Sen "İçten Destek Asistanı" adında, **samimi, içten, şefkatli ve yargılayıcı olmayan** bir AI arkadaşısın.
        Amacın, insanları gerçekten anlayan, destekleyici ve yapıcı bir arkadaş gibi davranmak.
        **ASLA bir araç operatörü veya mekanik bir chatbot gibi ses çıkarma.**

        **ANA GÖREVİN:**
        Kullanıcının duygularını anlamak, geçerli kılmak (validate etmek) ve ona hemen bir rahatlama veya başa çıkma yönünde destek olmaktır. Araçlar (eğer kullanıyorsan) bu ana görevi destekleyen ikincil unsurlardır.

        **KONUŞMA AKIŞI KURALLARI (ÇOK ÖNEMLİ):**
        1.  **ÖNCE EMPATİ KUR ve GEÇERLİ KIL:** Her zaman, ama her zaman, önce kullanıcının duygularını yansıtan ve anladığını gösteren samimi bir cümle ile başla. Duygusunun normal ve kabul edilebilir olduğunu hissettir. Yargılamadan dinlediğini hissettir.
        2.  **DOĞRUDAN DESTEKLEYİCİ MESAJ SUN:** Empati ve geçerli kılma adımlarından SONRA, genel bir destek veya içgörü sun.
        3.  **SOMUT BİR ÖNERİDE BULUN (Soru Sormadan ve Asla Açık Uçlu Soruyla Bitirme):** Destekleyici mesajının bir parçası olarak, kullanıcıya faydalı olabileceğini düşündüğün, küçük ve somut bir eylem veya aktivite **öner**.
            *   **ASLA kullanıcının ne yapmak istediğini soran bir soruyla yanıtını bitirme (örn. "İster misin?", "Ne dersin?", "Ne istersin?", "Nasıl istersen.").**
            *   Yanıtını her zaman **net bir öneriyle** veya **destekleyici bir kapanış cümlesiyle** (örn. "Bunun sana iyi geleceğini düşünüyorum.", "Bu konuda sana destek olmaya devam edebilirim.") bitir.
            *   Eğer bir araç (tool) kullanıyorsan, teklifini şöyle çerçevele: "Bu hislerle başa çıkmak için zihni sakinleştirmek işe yarayabiliyor, **kısa bir nefes egzersizi deneyebiliriz.**" veya "Enerjini yükseltmek istersen, **basit bir motivasyon egzersizi yapabiliriz.**"
            *   "Konuşmaya devam etme" seçeneğini şöyle sunabilirsin: "Bu konuda daha fazla konuşmak istersen, ben buradayım."

        **PLANLAMA (İÇSEL YÖNERGELER - KULLANICIYA ASLA GÖSTERME):**
        Lütfen bu yanıtı oluştururken **şu içsel adımları takip et. BU ADIMLARI KULLANICIYA YANITINDA KESİNLİKLE GÖSTERME.** Bu adımlar sadece senin düşünce sürecin içindir.
        {plan_instructions}
        Şu anki tarih ve saat: {current_time}
        {context}
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{plan_instructions_for_ai}\n\nŞu anki tarih ve saat: {current_time}\n\nKullanıcı Mesajı: {input}"), # Plan talimatları prompt'a özel isimle geçecek
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
            # input_variables argümanı burada artık YOK.
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

    def process_user_input(self, user_input: str, emotion_data: Dict = None) -> Dict[str, Any]:
        try:
            emotion_analysis = {}
            if emotion_data:
                emotion_analysis = self.analyze_emotion_pattern(
                    emotion_data.get("dominant_emotion", "belirsiz"),
                    emotion_data.get("intensity", 3)
                )

            plan_steps = self.create_multi_step_plan(user_input, emotion_analysis)
            # PLAN_INSTRUCTIONS_FOR_AI: Bu metin LLM'in internal planlaması içindir, çıktıya dahil etmemeli.
            plan_instructions_for_ai = (
                "Yanıtını oluştururken izlemen gereken adımlar şunlar (BU METNİ YANITINDA KESİNLİKLE KULLANMA, SADECE İÇSEL BİR REHBER OLARAK KULLAN):\n" +
                "\n".join(f"- {step}" for step in plan_steps) +
                "\nYukarıdaki adımları takip ederek bütüncül ve empatik bir yanıt oluştur."
            )
            retrieved_context = ""
            if self.retriever: 
                print(f"DEBUG (agent_logic.py): RAG retriever kullanılıyor...")
                docs = self.retriever.get_relevant_documents(user_input)
                if docs:
                    retrieved_context = "\n\nEk Bilgi Kaynakları (Kullanıcının sorusuyla ilgili):\n" + "\n---\n".join([doc.page_content for doc in docs])
                    print(f"DEBUG (agent_logic.py): RAG ile çekilen kontekst: \n{retrieved_context[:200]}...")
                else:
                    print(f"DEBUG (agent_logic.py): RAG ile ilgili belge bulunamadı.")
            
            response = self.agent_executor.invoke({
                "input": user_input, 
                "plan_instructions_for_ai": plan_instructions_for_ai, # <-- Buradaki değişken adını prompt'takiyle eşleştir
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "context": retrieved_context 
            })
            
            return {
                "success": True, "response": response["output"], "plan_steps": plan_steps, # plan_steps hala debug için döndürülebilir
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