from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

# Langchain import - eğer yoksa fallback
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    print("WARNING: langchain-google-genai not installed")

app = FastAPI()

# CORS headers manuel olarak ekliyoruz
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Global LLM instance
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None and HAS_LANGCHAIN:
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                _llm_instance = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    google_api_key=api_key,
                    temperature=0.7
                )
            except Exception as e:
                print(f"LLM init error: {e}")
    return _llm_instance

class PropertyRequest(BaseModel):
    description: str
    listing_type: str

# Health check endpoint
@app.get("/api")
@app.get("/api/")
async def root():
    api_key = os.getenv("GOOGLE_API_KEY", "")
    return {
        "status": "healthy",
        "message": "Immo-Agent Pro API is running",
        "has_api_key": bool(api_key),
        "langchain_available": HAS_LANGCHAIN,
        "endpoints": ["/api/test", "/api/generate"]
    }

@app.get("/api/test")
async def test():
    api_key = os.getenv("GOOGLE_API_KEY", "")
    llm = get_llm()
    
    return {
        "status": "ok",
        "message": "API funktioniert!",
        "environment": {
            "has_api_key": bool(api_key),
            "api_key_length": len(api_key) if api_key else 0,
            "langchain_available": HAS_LANGCHAIN,
            "llm_initialized": llm is not None
        }
    }

@app.post("/api/generate")
async def generate(request: PropertyRequest):
    try:
        # Validations
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GOOGLE_API_KEY nicht konfiguriert. Bitte in Vercel Environment Variables hinzufügen."
            )
        
        if not HAS_LANGCHAIN:
            raise HTTPException(
                status_code=500,
                detail="langchain-google-genai ist nicht installiert"
            )
        
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
        
        # Generate content
        prompt = f"""Du bist ein professioneller deutscher Immobilienmakler.

Erstelle einen PROFESSIONELLEN deutschen Immobilien-Anzeigentext.

IMMOBILIE:
- Typ: {request.listing_type}
- Details: {request.description}

STRUKTUR:
1. 🏠 ÜBERSCHRIFT (attraktiv, max 10 Wörter)
2. ✨ HIGHLIGHTS (3-5 Stichpunkte)
3. 📝 BESCHREIBUNG (2-3 Absätze, professionell)
4. 📍 LAGE (Standortvorteile)
5. 📞 KONTAKT (Call-to-Action)

Schreibe auf DEUTSCH, professionell und verkaufsorientiert."""

        print(f"Generating for: {request.listing_type}")
        response = llm.invoke(prompt)
        print("Generated successfully")
        
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
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Generierung: {str(e)}"
        )

# Vercel handler
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    print("WARNING: mangum not installed")
    handler = None
