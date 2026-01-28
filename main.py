import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# API anahtarlarını Vercel'den güvenli şekilde alıyoruz
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

class PropertyRequest(BaseModel):
    description: str
    listing_type: str

@app.post("/generate")
async def generate_content(request: PropertyRequest):
    try:
        prompt = f"Analiz et: {request.description}. Tip: {request.listing_type}. Almanca profesyonel emlak ilanı yaz."
        response = llm.invoke(prompt)
        return {"status": "success", "text": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "running"}