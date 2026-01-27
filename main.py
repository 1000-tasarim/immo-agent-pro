import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
# DALL-E için (Gerçek üretimde açılır)
# from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

# --- 1. AYARLAR & KURULUM ---
app = FastAPI(title="Immo-Agent DACH API", version="1.0")

# API Anahtarlarını buraya girin
os.environ["GOOGLE_API_KEY"] = "BURAYA_GEMINI_API_KEY"
os.environ["OPENAI_API_KEY"] = "BURAYA_OPENAI_KEY"

# Model Tanımı (Gemini 1.5 Pro)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)

# --- 2. VERİ MODELLERİ (Girdi Kapısı) ---
class PropertyRequest(BaseModel):
    description: str          # İlan metni veya PDF'ten çekilen ham metin
    listing_type: str         # "rent" (Kiralık) veya "sale" (Satılık)
    platform: str = "instagram"
    has_images: bool = False  # Kullanıcı kendi resmini yükledi mi?

# --- 3. GÖRSEL ÜRETİM MOTORU (Çift Modlu) ---
def generate_dual_images(desc: str, listing_type: str):
    """
    Eğer kullanıcının resmi yoksa, DALL-E 3 ile hem Eşyalı hem Boş resim üretir.
    """
    # Kiralık/Satılık durumuna göre atmosfer ayarı
    mood = "Warm, cozy, ready to live in" if listing_type == "rent" else "High value, pristine condition, luxury investment"
    
    # Prompt 1: Sanal Dekorasyon (Staged)
    prompt_staged = f"Photorealistic interior design of {desc}. Style: Modern German, {mood}. Fully furnished, soft lighting. 4k resolution."
    
    # Prompt 2: Mimari (Empty)
    prompt_empty = f"Architectural photography of empty room: {desc}. Focus on space, flooring, high ceilings, white walls. Bright natural light. 4k."
    
    # Simülasyon (API Key olmadığı durumda hata vermemesi için)
    # Gerçek kullanımda: url = DallEAPIWrapper().run(prompt)
    return {
        "staged": "https://images.unsplash.com/photo-1502005229762-cf1afd386884?auto=format&fit=crop&w=800&q=80", # Örnek
        "empty": "https://images.unsplash.com/photo-1493804714600-6edb1cd93a1f?auto=format&fit=crop&w=800&q=80"   # Örnek
    }

# --- 4. AJAN EKİBİ (CREW) ---
def create_crew(desc: str, listing_type: str, platform: str):
    
    # Hedef Kitle Belirleme
    target_audience = "Kiracılar (Tenants)" if listing_type == "rent" else "Yatırımcılar (Investors)"
    
    # Ajan 1: Analist
    analyst = Agent(
        role='Real Estate Analyst (DACH)',
        goal=f'Veriyi analiz et ve {target_audience} için en önemli satış noktasını (USP) bul.',
        backstory='Almanya emlak piyasasında uzman, yasalara (Energieausweis vb.) hakim bir analistsin.',
        allow_delegation=False,
        llm=llm
    )

    # Ajan 2: Yazar
    writer = Agent(
        role='Social Media Copywriter (German)',
        goal=f'{platform} platformu için viral, Almanca ve "Sie" hitaplı metin yaz.',
        backstory='İnsan psikolojisinden anlayan, emojileri dozunda kullanan profesyonel yazar.',
        allow_delegation=False,
        llm=llm
    )

    # Görevler
    task1 = Task(
        description=f"İlanı analiz et: {desc}. Tip: {listing_type}. Hedef kitleye uygun avantajları çıkar.",
        agent=analyst
    )
    
    task2 = Task(
        description="Analist raporuna göre post metnini yaz. Başlık, Hikaye, CTA ve Hashtagler olsun.",
        agent=writer
    )

    return Crew(agents=[analyst, writer], tasks=[task1, task2], process=Process.sequential)

# --- 5. API UÇ NOKTASI (Sihirli Buton) ---
@app.post("/generate")
def generate_content(request: PropertyRequest):
    try:
        # 1. Metin Üretimi
        crew = create_crew(request.description, request.listing_type, request.platform)
        text_result = crew.kickoff()
        
        # 2. Görsel Üretimi (Eğer kullanıcı yüklemediyse)
        images = {}
        if not request.has_images:
            images = generate_dual_images(request.description, request.listing_type)
            
        return {
            "status": "success",
            "text": str(text_result),
            "images": images,
            "mode": request.listing_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)