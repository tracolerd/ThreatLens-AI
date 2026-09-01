import os
import base64
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

async def check_virustotal(url: str) -> dict:
    if not VT_API_KEY or VT_API_KEY == "your_virustotal_api_key_here":
        return {"malicious_votes": 0, "status": "VT API key not configured"}
    
    # VirusTotal v3 requires base64 url safe encoding without padding (=)
    url_bytes = url.encode("utf-8")
    url_id = base64.urlsafe_b64encode(url_bytes).decode("utf-8").strip("=")
    
    headers = {"x-apikey": VT_API_KEY}
    async with httpx.AsyncClient() as httpx_client:
        try:
            response = await httpx_client.get(
                f"https://www.virustotal.com/api/v3/urls/{url_id}",
                headers=headers,
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                return {"malicious_votes": malicious, "suspicious_votes": suspicious}
            elif response.status_code == 404:
                return {"malicious_votes": 0, "status": "URL not found in VT database"}
            else:
                return {"error": f"VT API Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

async def analyze_with_openai(url: str, features: dict, vt_results: dict) -> dict:
    if not client:
        return {
            "threat_score": 50,
            "status": "SUSPICIOUS",
            "reasons": ["OpenAI API key missing. Default fallback score applied."]
        }
    
    prompt = f"""
    You are an elite cybersecurity expert specialized in phishing detection. 
    Analyze the following URL and telemetry data to assess phishing/malicious risk.
    
    URL: {url}
    Lexical Features: {features}
    VirusTotal Results: {vt_results}
    
    Provide your output strictly in the following JSON format without any markdown wrappers or extra text:
    {{
        "threat_score": <integer between 0 and 100>,
        "status": "<SAFE, SUSPICIOUS, or DANGEROUS>",
        "reasons": [<array of 2-3 concise string reasons explaining the verdict>]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "threat_score": 40,
            "status": "SUSPICIOUS",
            "reasons": [f"AI analysis failed due to error: {str(e)}"]
        }