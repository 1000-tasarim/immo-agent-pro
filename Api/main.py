import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# CORS middleware ekle (frontend için önemli)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API anahtarını kontrol et
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

class PropertyRequest(BaseModel):
    description: str
    listing_type: str

@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "message": "API is running",
        "endpoints": {
            "generate": "/generate (POST)"
        }
    }

@app.post("/api/generate")  # /api/ prefix ekledim
async def generate_content(request: PropertyRequest):
    try:
        # Input validation
        if not request.description or len(request.description.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Beschreibung muss mindestens 10 Zeichen lang sein"
            )
        
        # Geliştirilmiş prompt
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
        
        # AI çağrısı (timeout koruması ile)
        response = llm.invoke(prompt)
        
        return {
            "status": "success",
            "data": {
                "generated_text": response.content,
                "listing_type": request.listing_type
            }
        }
        
    except Exception as e:
        print(f"Error in generate_content: {str(e)}")  # Logging
        raise HTTPException(
            status_code=500, 
            detail=f"Fehler bei der Generierung: {str(e)}"
        )

# Test endpoint
@app.get("/api/test")
async def test():
    return {"message": "API funktioniert!", "status": "ok"}