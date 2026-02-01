import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global
_llm = None
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

class PropertyRequest(BaseModel):
    description: str
    listing_type: str

def get_llm():
    global _llm
    if _llm is not None:
        return _llm
    
    if not GOOGLE_API_KEY:
        return None
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        _llm = genai.GenerativeModel("gemini-pro")
        return _llm
    except Exception as e:
        print(f"ERROR: LLM init failed: {e}")
        return None

@app.get("/")
@app.get("/api")
@app.get("/api/")
def root():
    return {"status": "ok", "message": "Immo-Agent Pro API"}

@app.get("/api/test")
def test():
    llm = get_llm()
    return {
        "status": "ok",
        "message": "API funktioniert!",
        "environment": {
            "has_api_key": bool(GOOGLE_API_KEY),
            "api_key_length": len(GOOGLE_API_KEY) if GOOGLE_API_KEY else 0,
            "llm_initialized": llm is not None
        }
    }

@app.post("/api/generate")
def generate(request: PropertyRequest):
    try:
        if not GOOGLE_API_KEY:
            raise HTTPException(500, "GOOGLE_API_KEY nicht konfiguriert")
        
        if not request.description or len(request.description.strip()) < 10:
            raise HTTPException(400, "Beschreibung zu kurz (min. 10 Zeichen)")
        
        llm = get_llm()
        if not llm:
            raise HTTPException(500, "LLM konnte nicht initialisiert werden")
        
        prompt = f"""Du bist ein professioneller deutscher Immobilienmakler.

Erstelle einen PROFESSIONELLEN Immobilien-Anzeigentext auf Deutsch.

IMMOBILIE:
- Typ: {request.listing_type}
- Details: {request.description}

STRUKTUR:
1. 🏠 ÜBERSCHRIFT (attraktiv, max 10 Wörter)
2. ✨ HIGHLIGHTS (3-5 Stichpunkte)
3. 📝 BESCHREIBUNG (2-3 Absätze)
4. 📍 LAGE (Standortvorteile)
5. 📞 KONTAKT (Call-to-Action)

Schreibe auf DEUTSCH, professionell und verkaufsorientiert."""

        print(f"Generating for: {request.listing_type}")
        response = llm.generate_content(prompt)
        print("Generated successfully")
        
        return {
            "status": "success",
            "data": {
                "generated_text": response.text,
                "listing_type": request.listing_type
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(500, f"Fehler: {str(e)}")
