from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from typing import Dict, List, Any
import json
from datetime import datetime
from tools import get_agent_tools

class EmotionalSupportAgent:
    """
    Destekleyici Mini Terapi Asistanı - Agent Mimarisi
    
    Bu agent şu yeteneklere sahiptir:
    1. Hafıza: Önceki konuşmaları hatırlar
    2. Tool Kullanımı: Meditasyon, egzersiz, kaynak önerileri
    3. Çok Adımlı Planlama: Karmaşık durumlarda adım adım çözüm
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Hafıza sistemi - önceki konuşmaları hatırlar
        self.memory = ConversationBufferMemory(

            memory_key="chat_history",
            return_messages=True,
            output_key="output",
            input_key="input",
        )
        
        # Agent'ın kullanabileceği araçları yükle
        self.tools = get_agent_tools()
        
        # Agent prompt'unu oluştur
        self.prompt = self._create_agent_prompt()
        
        # Agent'ı oluştur
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Agent executor'ı oluştur
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
        
        # Kullanıcı profili ve duygu geçmişi
        self.user_profile = {
            "emotion_history": [],
            "preferred_support_types": [],
            "crisis_indicators": []
        }
    
    def _create_agent_prompt(self) -> ChatPromptTemplate:
        """
        Agent için özel prompt oluşturur
        """
        system_message = """
        Sen "Destekleyici Mini Terapi Asistanı" adında bir AI agent'sın. Görevin kullanıcıların duygusal destek sağlamak.

YETENEKLERİN:
1. 🧠 HAFIZA: Önceki konuşmaları hatırlayarak kişiselleştirilmiş destek veriyorsun
2. 🛠️ ARAÇ KULLANIMI: Gerektiğinde meditasyon, egzersiz, kaynak önerebiliyorsun
3. 📋 PLANLAMA: Karmaşık durumlarda adım adım çözüm planı yapabiliyorsun

YAKLAŞIMIN:
- Empati ve anlayış göster
- Yargılamadan dinle
- Önceki konuşmaları referans al
- Gerektiğinde araçları kullan
- Kriz durumlarında profesyonel yardım öner

ÖNEMLİ: Eğer kullanıcı ciddi depresyon, intihar düşünceleri veya kriz belirtileri gösteriyorsa,
mutlaka profesyonel yardım almasını öner ve uygun araçları kullan.

Şu anki tarih ve saat: {current_time}
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        prompt = prompt.partial(current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        
        return prompt
    
    def analyze_emotion_pattern(self, current_emotion: str, intensity: int) -> Dict[str, Any]:
        """
        Kullanıcının duygu geçmişini analiz eder
        """
        # Mevcut duyguyu geçmişe ekle
        emotion_entry = {
            "emotion": current_emotion,
            "intensity": intensity,
            "timestamp": datetime.now().isoformat()
        }
        self.user_profile["emotion_history"].append(emotion_entry)
        
        # Son 5 duyguyu analiz et
        recent_emotions = self.user_profile["emotion_history"][-5:]
        
        analysis = {
            "pattern_detected": False,
            "trend": "stable",
            "recommendations": [],
            "crisis_risk": "low"
        }
        
        if len(recent_emotions) >= 3:
            # Yoğunluk trendini kontrol et
            intensities = [e["intensity"] for e in recent_emotions]
            if all(i >= 4 for i in intensities[-3:]):
                analysis["trend"] = "worsening"
                analysis["crisis_risk"] = "medium"
                analysis["recommendations"].append("professional_help")
            elif all(i <= 2 for i in intensities[-3:]):
                analysis["trend"] = "improving"
            
            # Tekrarlayan duygu kontrolü
            emotions = [e["emotion"] for e in recent_emotions]
            if emotions.count(current_emotion) >= 3:
                analysis["pattern_detected"] = True
                analysis["recommendations"].append("pattern_intervention")
        
        return analysis
    
    def create_multi_step_plan(self, user_input: str, emotion_analysis: Dict) -> List[str]:
        """
        Karmaşık durumlar için çok adımlı plan oluşturur
        """
        plan_steps = []
        
        # 1. Durum değerlendirmesi
        plan_steps.append("🔍 Duygusal durumunu analiz ediyorum")
        
        # 2. Acil müdahale gerekli mi?
        if emotion_analysis["crisis_risk"] == "high":
            plan_steps.append("🚨 Acil destek kaynakları sağlıyorum")
            plan_steps.append("📞 Profesyonel yardım öneriyorum")
        
        # 3. Uygun araçları belirle
        if "stres" in user_input.lower() or "endişe" in user_input.lower():
            plan_steps.append("🧘 Rahatlatıcı teknikler öneriyorum")
        
        if "motivasyon" in user_input.lower() or "enerji" in user_input.lower():
            plan_steps.append("⚡ Motivasyon artırıcı egzersizler öneriyorum")
        
        # 4. Kişiselleştirilmiş mesaj
        plan_steps.append("💙 Kişiselleştirilmiş destek mesajı hazırlıyorum")
        
        # 5. Takip planı
        if emotion_analysis["pattern_detected"]:
            plan_steps.append("📊 Duygu takip planı oluşturuyorum")
        
        return plan_steps
    
    def process_user_input(self, user_input: str, emotion_data: Dict = None) -> Dict[str, Any]:
        """
        Kullanıcı girdisini işler ve agent yanıtı üretir
        """
        try:
            # Duygu analizi yap
            emotion_analysis = {}
            if emotion_data:
                emotion_analysis = self.analyze_emotion_pattern(
                    emotion_data.get("selected_emotion", "belirsiz"),
                    emotion_data.get("intensity", 3)
                )
            
            # Çok adımlı plan oluştur
            plan_steps = self.create_multi_step_plan(user_input, emotion_analysis)
            

            # Agent'ı çalıştır
            response = self.agent_executor.invoke({
                "input": user_input,
            })
            
            return {
                "success": True,
                "response": response["output"],
                "plan_steps": plan_steps,

            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_response": "Üzgünüm, şu anda teknik bir sorun yaşıyorum. Lütfen tekrar deneyin."
            }
    
    def _extract_tools_used(self, response: Dict) -> List[str]:
        """
        Kullanılan araçları çıkarır
        """
        # Bu basit bir implementasyon, gerçek kullanımda daha detaylı olabilir
        tools_used = []
        if "intermediate_steps" in response:
            for step in response["intermediate_steps"]:
                if hasattr(step, 'tool'):
                    tools_used.append(step.tool)
        return tools_used
    
    def _get_memory_summary(self) -> str:
        """
        Hafıza özetini döndürür
        """
        messages = self.memory.chat_memory.messages
        if len(messages) > 0:
            return f"Son {len(messages)} mesaj hafızada saklanıyor"
        return "Henüz hafızada mesaj yok"
    
    def clear_memory(self):
        """
        Hafızayı temizler
        """
        self.memory.clear()
        self.user_profile["emotion_history"] = []
    
    def get_user_profile_summary(self) -> Dict[str, Any]:
        """
        Kullanıcı profil özetini döndürür
        """
        return {
            "total_conversations": len(self.memory.chat_memory.messages) // 2,
            "emotion_history_count": len(self.user_profile["emotion_history"]),
            "recent_emotions": self.user_profile["emotion_history"][-3:] if self.user_profile["emotion_history"] else [],
            "memory_summary": self._get_memory_summary()
        }