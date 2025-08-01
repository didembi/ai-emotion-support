from langchain.tools import Tool
from typing import List, Dict, Any
import json
import random

def suggest_meditation_tool(input_text: str) -> str:
    """
    Kullanıcının durumuna göre meditasyon önerir
    """
    meditations = {
        "stres": {
            "title": "Stres Azaltıcı Nefes Meditasyonu",
            "duration": "10 dakika",
            "description": "Derin nefes teknikleriyle stresi azaltın",
            "link": "https://www.youtube.com/watch?v=YRPh_GaiL8s",
            "instructions": "4 saniye nefes alın, 7 saniye tutun, 8 saniye verin"
        },
        "endişe": {
            "title": "Endişe Azaltıcı Farkındalık Meditasyonu",
            "duration": "15 dakika",
            "description": "Endişeli düşünceleri sakinleştirin",
            "link": "https://www.youtube.com/watch?v=ZToicYcHIOU",
            "instructions": "Düşüncelerinizi yargılamadan gözlemleyin"
        },
        "üzüntü": {
            "title": "Şefkatli Farkındalık Meditasyonu",
            "duration": "12 dakika",
            "description": "Kendinize karşı şefkatli olun",
            "link": "https://www.youtube.com/watch?v=sz7cpV7ERsM",
            "instructions": "Kendinize nazik sözler söyleyin"
        },
        "genel": {
            "title": "Temel Farkındalık Meditasyonu",
            "duration": "8 dakika",
            "description": "Genel rahatlama için basit meditasyon",
            "link": "https://www.youtube.com/watch?v=inpok4MKVLM",
            "instructions": "Nefesinize odaklanın ve şu ana gelmeye çalışın"
        }
    }
    
    # Girdi metnine göre uygun meditasyonu seç
    selected_meditation = meditations["genel"]  # varsayılan
    
    input_lower = input_text.lower()
    if "stres" in input_lower or "gergin" in input_lower:
        selected_meditation = meditations["stres"]
    elif "endişe" in input_lower or "kaygı" in input_lower or "korku" in input_lower:
        selected_meditation = meditations["endişe"]
    elif "üzgün" in input_lower or "depresif" in input_lower or "kötü" in input_lower:
        selected_meditation = meditations["üzüntü"]
    
    return f"""
🧘‍♀️ **Önerilen Meditasyon:**

**{selected_meditation['title']}**
⏱️ Süre: {selected_meditation['duration']}
📝 Açıklama: {selected_meditation['description']}

🎯 **Nasıl Yapılır:**
{selected_meditation['instructions']}

🔗 **Rehberli Meditasyon Linki:**
{selected_meditation['link']}

💡 **İpucu:** Sessiz bir ortam bulun ve rahat bir pozisyonda oturun.
"""

def suggest_breathing_exercise(input_text: str) -> str:
    """
    Nefes egzersizleri önerir
    """
    exercises = [
        {
            "name": "4-7-8 Nefes Tekniği",
            "steps": [
                "4 saniye boyunca burnunuzdan nefes alın",
                "7 saniye nefesi tutun",
                "8 saniye boyunca ağzınızdan nefesi verin",
                "Bu döngüyü 4 kez tekrarlayın"
            ],
            "benefit": "Anksiyete ve stresi hızla azaltır"
        },
        {
            "name": "Karın Nefesi",
            "steps": [
                "Bir elinizi göğsünüze, diğerini karnınıza koyun",
                "Yavaşça burnunuzdan nefes alın, karnınız şişsin",
                "Ağzınızdan yavaşça nefesi verin, karnınız çökşün",
                "5-10 dakika boyunca devam edin"
            ],
            "benefit": "Derin rahatlama ve sakinlik sağlar"
        }
    ]
    
    exercise = random.choice(exercises)
    
    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(exercise['steps'])])
    
    return f"""
🫁 **Önerilen Nefes Egzersizi:**

**{exercise['name']}**

📋 **Adımlar:**
{steps_text}

✨ **Faydası:** {exercise['benefit']}

⚠️ **Uyarı:** Baş dönmesi hissederseniz normal nefes alışınıza dönün.
"""

def suggest_physical_activity(input_text: str) -> str:
    """
    Fiziksel aktivite önerileri
    """
    activities = {
        "düşük_enerji": [
            "5 dakikalık yavaş yürüyüş",
            "Hafif germe egzersizleri",
            "Yoga pozları (çocuk pozu, kedi-inek)",
            "Balkon veya pencerede durarak derin nefes alma"
        ],
        "orta_enerji": [
            "15 dakikalık hızlı yürüyüş",
            "Dans etme (sevdiğiniz müzikle)",
            "Merdiven çıkma-inme",
            "Basit kalistenik hareketler"
        ],
        "yüksek_enerji": [
            "30 dakikalık koşu",
            "Bisiklet sürme",
            "Yüzme",
            "Spor salonu antrenmanı"
        ]
    }
    
    # Girdi metnine göre enerji seviyesini tahmin et
    input_lower = input_text.lower()
    if "yorgun" in input_lower or "enerji" in input_lower or "bitkin" in input_lower:
        energy_level = "düşük_enerji"
    elif "aktif" in input_lower or "hareket" in input_lower:
        energy_level = "yüksek_enerji"
    else:
        energy_level = "orta_enerji"
    
    suggested_activities = activities[energy_level]
    activities_text = "\n".join([f"• {activity}" for activity in suggested_activities])
    
    return f"""
🏃‍♀️ **Önerilen Fiziksel Aktiviteler:**

{activities_text}

💡 **Neden Faydalı:**
• Endorfin salgılanmasını artırır
• Stresi azaltır
• Ruh halini iyileştirir
• Enerji seviyesini dengeler

⭐ **İpucu:** Küçük adımlarla başlayın, kendinizi zorlamayın.
"""

def suggest_self_care_activities(input_text: str) -> str:
    """
    Öz bakım aktiviteleri önerir
    """
    activities = [
        "Sıcak bir duş veya banyo yapın",
        "Sevdiğiniz bir kitabı okuyun",
        "Rahatlatıcı müzik dinleyin",
        "Günlük yazın",
        "Sevdiğiniz bir çay veya kahve için",
        "Arkadaşınızla telefonda konuşun",
        "Doğada zaman geçirin",
        "Yaratıcı bir aktivite yapın (çizim, yazı, müzik)",
        "Erken yatıp kaliteli uyku alın",
        "Besleyici bir yemek hazırlayın"
    ]
    
    selected_activities = random.sample(activities, 5)
    activities_text = "\n".join([f"• {activity}" for activity in selected_activities])
    
    return f"""
🌸 **Öz Bakım Önerileri:**

{activities_text}

💝 **Hatırlatma:**
Öz bakım lüks değil, ihtiyaçtır. Kendinize zaman ayırmak, başkalarına daha iyi bakabilmenizi sağlar.

🎯 **Bugün için seçin:** Listeden bir tanesini seçip kendinize hediye edin.
"""

def provide_crisis_resources(input_text: str) -> str:
    """
    Kriz durumları için kaynaklar sağlar
    """
    return """
🚨 **ACİL DESTEK KAYNAKLARI**

📞 **Kriz Hatları:**
• Yaşam Hattı: 182 (7/24 ücretsiz)
• TIHV Ruh Sağlığı: 0312 310 66 36
• Mavi Kalem: 444 0 632

🏥 **Acil Durumlar:**
• 112 - Acil Sağlık Hizmetleri
• En yakın hastane acil servisi

💙 **Online Destek:**
• 7cups.com - Ücretsiz duygusal destek
• Betterhelp.com - Online terapi

⚠️ **ÖNEMLİ:**
Eğer kendinize zarar verme düşünceleriniz varsa, lütfen hemen profesyonel yardım alın.
Yalnız değilsiniz ve yardım almak cesaret gerektirir.

🤝 **Güvenilir Kişiler:**
Aile üyeleriniz, yakın arkadaşlarınız veya güvendiğiniz kişilerle konuşmayı unutmayın.
"""

def suggest_professional_help(input_text: str) -> str:
    """
    Profesyonel yardım önerileri
    """
    return """
👨‍⚕️ **PROFESYONEL YARDIM ÖNERİLERİ**

🎯 **Ne Zaman Profesyonel Yardım Almalı:**
• Duygusal zorluklar 2 haftadan fazla sürüyorsa
• Günlük yaşamınızı etkiliyorsa
• Uyku, iştah veya enerji seviyenizde değişiklikler varsa
• Kendinizi izole ediyorsanız
• Başa çıkma stratejileriniz işe yaramıyorsa

🏥 **Profesyonel Seçenekler:**
• Psikolog: Konuşma terapisi, davranışsal teknikler
• Psikiyatrist: Medikal değerlendirme ve ilaç tedavisi
• Psikolojik Danışman: Yaşam koçluğu ve rehberlik
• Aile Danışmanı: İlişki ve aile sorunları

💰 **Uygun Fiyatlı Seçenekler:**
• Üniversite psikoloji bölümleri (stajyer terapistler)
• Belediye ruh sağlığı merkezleri
• SGK kapsamındaki hastaneler
• Online terapi platformları

📋 **İlk Randevu İçin:**
• Semptomlarınızı not edin
• Sorularınızı hazırlayın
• Açık ve dürüst olun
• Sabırlı olun - iyileşme zaman alır

💪 **Hatırlatma:** Yardım istemek güçlülük işaretidir, zayıflık değil.
"""

def get_agent_tools() -> List[Tool]:
    """
    Agent'ın kullanabileceği tüm araçları döndürür
    """
    tools = [
        Tool(
            name="MeditationSuggestion",
            func=suggest_meditation_tool,
            description="Kullanıcı stresli, endişeli veya rahatlama ihtiyacı duyduğunda meditasyon önerir. Girdi: kullanıcının duygusal durumu"
        ),
        Tool(
            name="BreathingExercise",
            func=suggest_breathing_exercise,
            description="Anksiyete, panik atak veya hızlı rahatlama ihtiyacında nefes egzersizleri önerir. Girdi: kullanıcının mevcut durumu"
        ),
        Tool(
            name="PhysicalActivity",
            func=suggest_physical_activity,
            description="Depresyon, düşük enerji veya ruh hali iyileştirme için fiziksel aktivite önerir. Girdi: kullanıcının enerji seviyesi ve durumu"
        ),
        Tool(
            name="SelfCareActivities",
            func=suggest_self_care_activities,
            description="Genel öz bakım ve kendine iyi bakma için aktiviteler önerir. Girdi: kullanıcının ihtiyaçları"
        ),
        Tool(
            name="CrisisResources",
            func=provide_crisis_resources,
            description="Kriz durumları, intihar düşünceleri veya acil yardım ihtiyacında kaynaklar sağlar. Girdi: kriz durumu açıklaması"
        ),
        Tool(
            name="ProfessionalHelp",
            func=suggest_professional_help,
            description="Uzun süreli sorunlar veya ciddi ruh sağlığı endişeleri için profesyonel yardım önerir. Girdi: kullanıcının durumu"
        )
    ]
    
    return tools