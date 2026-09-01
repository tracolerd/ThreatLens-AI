from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from utils import extract_lexical_features
from services import check_virustotal, analyze_with_openai

app = FastAPI(
    title="ThreatLens-AI API",
    description="Backend for AI-Powered Phishing & Malicious URL Scanner",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: HttpUrl

class ScanResponse(BaseModel):
    threat_score: int
    status: str
    reasons: list[str]

@app.get("/")
async def health_check():
    return {"status": "operational", "service": "ThreatLens-AI"}

@app.post("/api/v1/scan", response_model=ScanResponse)
async def scan_url(request: ScanRequest):
    target_url = str(request.url)
    
    if not target_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    try:
        # Step 1: Extract Lexical Features
        features = extract_lexical_features(target_url)
        
        # Step 2: Query VirusTotal Threat Intelligence
        vt_data = await check_virustotal(target_url)
        
        # Step 3: OpenAI Contextual Phishing Analysis
        ai_assessment = await analyze_with_openai(target_url, features, vt_data)
        
        return ScanResponse(
            threat_score=ai_assessment.get("threat_score", 0),
            status=ai_assessment.get("status", "SAFE"),
            reasons=ai_assessment.get("reasons", ["No specific threats detected."])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)