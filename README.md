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
