<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:071B20,50:0F766E,100:0B1220&height=190&section=header&text=ThreatLens%20AI&fontSize=42&fontColor=F1F5F9&fontAlignY=38&animation=fadeIn&desc=A%20multi-signal%20phishing%20and%20malicious%20URL%20scanning%20prototype&descAlignY=61&descSize=15" alt="ThreatLens AI animated project banner" width="100%" />
</p>

<div align="center">

# 🛡️ ThreatLens-AI
**AI-Powered Phishing & Malicious URL Scanner**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Manifest V3](https://img.shields.io/badge/Chrome-Extension-F4B400.svg?logo=google-chrome)](https://developer.chrome.com/docs/extensions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-stack cybersecurity extension that evaluates URL threats in real-time. It calculates a unified threat score by combining client-side URL lexical analysis, VirusTotal threat intelligence, and OpenAI GPT-4o-mini contextual reasoning.

</div>

---

## 🚀 System Architecture

```mermaid
sequenceDiagram
    actor User
    participant Chrome Ext
    participant FastAPI Backend
    participant VirusTotal API
    participant OpenAI API

    User->>Chrome Ext: Clicks "Scan This Page"
    Chrome Ext->>FastAPI Backend: POST /api/v1/scan {url}
    FastAPI Backend->>FastAPI Backend: Extract Lexical Features
    FastAPI Backend->>VirusTotal API: Query Threat Database
    VirusTotal API-->>FastAPI Backend: Return Malicious Votes
    FastAPI Backend->>OpenAI API: Contextual Phishing Prompt
    OpenAI API-->>FastAPI Backend: Threat Score & Reasons
    FastAPI Backend-->>Chrome Ext: JSON Response
    Chrome Ext->>User: Display Status (SAFE / SUSPICIOUS / DANGEROUS)
```
## ✨ Core Features

* **Real-time Tab Detection**: Automatically pulls the active URL from your Chrome tab using Manifest V3 APIs.
* **Lexical Feature Extraction**: Analyzes domain structure, IP presence, typosquatting keywords, and URL lengths.
* **VirusTotal Intelligence**: Queries global threat databases for reported domain flags.
* **AI Contextual Analysis**: Leverages LLMs to evaluate subtle phishing patterns and malicious intent.
* **Modern Dark UI**: Lightweight, responsive popup dashboard with clean visual threat indicators.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Frontend** | HTML5, CSS3, Vanilla JS | Chrome Extension (Manifest V3) |
| **Backend** | Python 3.11+, FastAPI | High-performance API server |
| **Server** | Uvicorn | ASGI web server implementation |
| **External APIs**| OpenAI, VirusTotal | Threat intelligence & LLM reasoning |

---

## ⚙️ Installation & Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone [https://github.com/tracolerd/ThreatLens-AI.git](https://github.com/tracolerd/ThreatLens-AI.git)
cd ThreatLens-AI/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
Environment Variables:
Create a .env file in the backend directory and add your API keys:
```bash
OPENAI_API_KEY=your_actual_openai_api_key
VIRUSTOTAL_API_KEY=your_actual_virustotal_api_key

# Start the Server:
uvicorn main:app --reload
```

### 2. Chrome Extension Setup
Open Google Chrome and navigate to chrome://extensions/.

Enable Developer mode (toggle at the top-right corner).

Click Load unpacked and select the extension/ directory from this project.

Pin ThreatLens-AI to your browser toolbar.

📡 API Endpoint Reference
POST /api/v1/scan

```bash
# Request:
{
  "url": "[https://example-phishing-site.com/login](https://example-phishing-site.com/login)"
}

# Response:
{
  "threat_score": 85,
  "status": "DANGEROUS",
  "reasons": [
    "Domain contains suspicious keyword 'login' with IP redirect.",
    "Flagged by 4 VirusTotal security vendors.",
    "OpenAI detected credential harvesting patterns in URL path."
  ]
}
```

🔒 Security & Privacy Notice
Note: URLs sent to the backend are evaluated transiently and are strictly not stored in any database. Sensitive query parameters are stripped during heuristic extraction to preserve user privacy.

---

## Author & Development

**Project author and solo developer:** [Nurul Faiyaz](https://github.com/tracolerd).

This project is independently developed and maintained by Nurul Faiyaz. AI-assisted tools may be used as part of the development workflow; the project author remains responsible for technical decisions, code review, validation, and maintenance.

