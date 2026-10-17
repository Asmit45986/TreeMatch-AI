# 🌲 GreenMind AI — Enterprise Multi-Dimensional Afforestation & Carbon-Credit Intelligence Platform

> **GreenMind AI** ek enterprise-grade environmental telemetry aur predictive intelligence platform hai. Ye system deep learning computer vision, high-dimensional machine learning, aur multi-scenario financial modeling ka upyog karke soil classification, optimal tree species selection, aur carbon credit yield estimation prime accuracy ke saath perform karta hai.

---

## 📌 Table of Contents
1. [System Overview](#-system-overview)
2. [Key Platform Features](#-key-platform-features)
3. [System Architecture](#-system-architecture)
4. [Tech Stack & Dependencies](#-tech-stack--dependencies)
5. [Directory Structure](#-directory-structure)
6. [Mathematical & Machine Learning Pipeline](#-mathematical--machine-learning-pipeline)
7. [Installation & Local Setup](#-installation--local-setup)
8. [API Documentation](#-api-documentation)
9. [Cloud Deployment Architecture](#-cloud-deployment-architecture)
10. [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## 🌟 System Overview

GreenMind AI environmental decision-making ko scientific data ke saath automate karta hai. System ke main objectives hain:
* **Soil Health Analysis:** Topsoil photos aur environmental metrics (pH, AQI, Temp) ko process karke soil texture aur quality detect karna.
* **Precision Species Matching:** Regional survival probability ke basis par top tree species suggest karna.
* **Carbon Credit & ROI Projections:** Forestry investments ke liye Net Present Value (NPV), Internal Rate of Return (IRR), aur carbon credit offset projections simulate karna.
* **High Availability:** Self-healing fallback dataset generation mechanism jo server response rate 100% rakhta hai.

---

## 🚀 Key Platform Features

| Feature | Description |
| :--- | :--- |
| **Soil CNN Classifier** | Computer Vision model jo topsoil structure aur organic profile analyze karta hai. |
| **10k Telemetry Matcher** | Soil pH, AQI, aur temperature dynamics par based machine learning matching engine. |
| **Multi-Scenario Carbon ROI** | Institutional investors ke liye multi-year yield simulation aur carbon credit estimation. |
| **Dynamic Fallback Engine** | Cold-start ya missing CSV files ke case mein dynamic data generation layer. |
| **Decoupled Architecture** | High-performance FastAPI REST backend connected with responsive Next.js frontend. |

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        NEXT.JS FRONTEND (Vercel)                       │
│                   Subdirectory: /greenmind-frontend                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                            HTTP REST / JSON API
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                        FASTAPI BACKEND (Render)                        │
│                        Python 3.11 Environment                         │
└──────┬────────────────────────────┬────────────────────────────┬───────┘
       │                            │                            │
┌──────▼──────────────┐   ┌─────────▼────────────┐   ┌───────────▼───────────┐
│ Computer Vision     │   │ Ecological Matching  │   │ Financial Modeling    │
│ Soil Classifier CNN │   │ Scikit-Learn Engine  │   │ Carbon ROI Simulator  │
└─────────────────────┘   └──────────────────────┘   └───────────────────────┘
🛠️ Tech Stack & Dependencies
Backend Engine (FastAPI)
Language: Python 3.11

Framework: FastAPI, Uvicorn

Data Processing & ML: scikit-learn, pandas, numpy

Image Processing: Pillow, python-multipart

Validation: pydantic

Frontend Application (Next.js)
Framework: Next.js 14 (App Router)

UI Components & Styling: React 18, Tailwind CSS, Lucide Icons

Data Fetching: Axios / Native Fetch API
TreeMatch-AI/
│
├── app/                          # FastAPI Backend Engine
│   ├── __init__.py
│   ├── main.py                   # App entrypoint, CORS & core routes
│   ├── models/                   # ML inference engines & pipelines
│   └── utils/                    # Math utilities & fallback generators
│
├── greenmind-frontend/           # Next.js Web Client Application
│   ├── app/                      # App router layout & dashboard pages
│   ├── public/                   # Static assets & brand media
│   ├── package.json              # Node dependencies & npm scripts
│   └── next.config.js            # Next.js build setup
│
├── datasets/                     # Ecological datasets (.gitignore managed)
├── requirements.txt              # Python production dependencies
├── .gitignore                    # Environment & heavy payload exclusions
└── README.md                     # System documentation

🧮 Mathematical & Machine Learning Pipeline
Soil Stress Matrix Analysis:$$\text{Stress Score} = f(\text{pH Error}) + g(\text{AQI Index}) + h(\Delta \text{Temp})$$Survival Probability Matrix:$$P(\text{Survival}) = \sigma(W_1 \cdot \text{SoilScore} + W_2 \cdot \text{ClimateMatch} + W_3 \cdot \text{pH suitability})$$Carbon Yield Calculation:$$\text{Carbon Offset (Tons)} = \text{Tree Count} \times \text{Growth Rate} \times \text{Sequestration Coefficient}$$

💻 Installation & Local Setup
Prerequisites
Python 3.11+

Node.js 18+ & npm

Git

Step 1: Clone Repository

git clone [https://github.com/Asmit45986/TreeMatch-AI.git](https://github.com/Asmit45986/TreeMatch-AI.git)
cd TreeMatch-AI

# Virtual environment create karein
python -m venv ai_env

# Virtual environment activate karein
# Windows:
ai_env\Scripts\activate
# Linux/Mac:
source ai_env/bin/activate

# Dependencies install karein
pip install -r requirements.txt

# Server run karein
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend directory mein jayein
cd greenmind-frontend

# Dependencies install karein
npm install

# Local environment variable set karein (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Next.js app start karein
npm run dev

API Documentation
1. System Status Check
Endpoint: GET /

{
  "status": "online",
  "system": "GreenMind AI Advanced Engine"
}

2. Prediction & Analysis EndpointEndpoint: POST /api/v1/predictContent-Type: multipart/form-dataPayload Parameters:image: Soil photo file (JPEG/PNG)ph: Soil pH level (float)aqi: Air Quality Index (float)temperature: Regional Temperature in °C (float)☁️ Cloud Deployment ArchitectureBackend Service (Render):Environment: Python 3.11Build Command: pip install -r requirements.txtStart Command: uvicorn app.main:app --host 0.0.0.0 --port $PORTEnvironment Variables: PYTHONPATH=., PYTHON_VERSION=3.11Live URL: https://treematch-ai-1.onrender.comFrontend Service (Vercel):Framework Preset: Next.jsRoot Directory: greenmind-frontendEnvironment Variables: NEXT_PUBLIC_API_URL=https://treematch-ai-1.onrender.com❓ Troubleshooting & FAQsIssue: Render Build Fails on NumPy C-Extension CompilationSolution: Render Environment variables mein PYTHON_VERSION = 3.11 set karein taaki pre-built wheels install ho sakein.Issue: Vercel Deploy Returns 404 NOT_FOUNDSolution: Vercel Settings $\rightarrow$ General mein Root Directory ko greenmind-frontend set karke Redeploy karein.