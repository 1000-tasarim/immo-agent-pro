import os
import sys

# FastAPI ve Pydantic
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError as e:
    print(f"ERROR: Failed to import FastAPI/Pydantic: {e}")
    sys.exit(1)

# FastAPI app
app = FastAPI()

# Global variables
_llm = None
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# CORS Middleware
@app.middleware("http")
async def cors_middleware(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Pydantic model
class PropertyRequest(BaseModel):
    description: str
    listing_type: str

# Lazy LLM loader
def get_llm():
    global _llm
    if _llm is not None:
        return _llm
    
    if not GOOGLE_API_KEY:
        return None
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        _llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7
        )
        return _llm
    except Exception as e:
        print(f"ERROR: LLM initialization failed: {e}")
        return None

# Health check endpoints
@app.get("/")
def root():
    return {"status": "ok", "message": "Immo-Agent Pro API"}

@app.get("/api")
def api_root():
    return {"status": "ok", "message": "Immo-Agent Pro API"}

@app.get("/api/")
def api_root_slash():
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
        # Validate API key
        if not GOOGLE_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="GOOGLE_API_KEY nicht konfiguriert"
            )
        
        # Validate input
        if not request.description or len(request.description.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Beschreibung muss mindestens 10 Zeichen lang sein"
            )
        
        # Get LLM
        llm = get_llm()
        if not llm:
            raise HTTPException(
                status_code=500,
                detail="LLM konnte nicht initialisiert werden"
            )
        
        # Generate prompt
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

        # Call LLM
        print(f"Generating content for: {request.listing_type}")
        response = llm.invoke(prompt)
        print("Content generated successfully")
        
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
        print(f"ERROR in generate: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler: {error_msg}"
        )

# Vercel handler - CRITICAL!
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
    print("Mangum handler initialized successfully")
except ImportError as e:
    print(f"WARNING: Mangum not available: {e}")
    # Fallback handler for local testing
    handler = None
except Exception as e:
    print(f"ERROR: Mangum initialization failed: {e}")
    handler = None
