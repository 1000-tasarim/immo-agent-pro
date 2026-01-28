import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API anahtarını kontrol et
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM'i lazy initialize et
_llm = None

def get_llm():
    global _llm
    if _llm is None and ChatGoogleGenerativeAI is not None:
        try:
            _llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.7
            )
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
    return _llm

class PropertyRequest(BaseModel):
    description: str
    listing_type: str

@app.get("/api/test")
@app.get("/test")
async def test():
    return {
        "message": "API funktioniert!", 
        "status": "ok",
        "has_api_key": GOOGLE_API_KEY is not None and len(GOOGLE_API_KEY) > 0,
        "langchain_available": ChatGoogleGenerativeAI is not None
    }

@app.post("/api/generate")
@app.post("/generate")
async def generate_content(request: PropertyRequest):
    try:
        # API key kontrolü
        if not GOOGLE_API_KEY:
            raise HTTPException(
                status_code=500, 
                detail="GOOGLE_API_KEY ist nicht konfiguriert"
            )
        
        llm = get_llm()
        if not llm:
            raise HTTPException(
                status_code=500, 
                detail="LLM konnte nicht initialisiert werden"
            )
        
        # Input validation
        if not request.description or len(request.description.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Beschreibung muss mindestens 10 Zeichen lang sein"
            )
        
        prompt = f"""
Du bist ein professioneller Immobilienmakler in Deutschland.

Aufgabe: Erstelle einen professionellen Immobilien-Anzeigentext auf Deutsch.

Immobiliendetails:
- Beschreibung: {request.description}
- Angebotstyp: {request.listing_type}

Bitte erstelle einen überzeugenden, professionellen Text mit:
1. Attraktiver Überschrift
2. Hauptmerkmale (3-5 Punkte)
3. Detaillierte Beschreibung
4. Lage-Highlights
5. Kontakt-Call-to-Action

Format: Strukturiert und verkaufsorientiert.
"""
        
        response = llm.invoke(prompt)
        
        return {
            "status": "success",
            "data": {
                "generated_text": response.content,
                "listing_type": request.listing_type
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        raise HTTPException(
            status_code=500, 
            detail=f"Fehler: {error_msg}"
        )

# Vercel serverless handler
handler = Mangum(app)