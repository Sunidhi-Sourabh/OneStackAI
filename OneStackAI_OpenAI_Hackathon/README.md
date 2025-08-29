# 🧠 OneStackAI — App + Agent (OpenAI Hackathon Edition)

A mobile-first AI tools hub designed for creators, developers, and neurodivergent minds who crave clarity, speed, and control.  
Built with 💡 [Sunidhi Sourabh](https://devpost.com/sunidhisourabh) — student founder, full-stack dev, and indie ecosystem architect.

---

## 🚀 Vision

To curate and unify 100+ AI tools into a single mobile/laptop/tab-first hub—designed for seamless access across diverse user needs, from productivity, creativity, utility, fashion, career, education to everyday doubts.  
OneStackAI empowers users to launch, explore, and flow—without friction or compromise.

---

## 🧩 Dual Submission Overview

This repo contains **two distinct builds**:

### 1. 🧠 OneStackAI App  
A scalable, privacy-first dashboard for discovering and launching AI tools.

### 2. 🤖 OneStackAI GPT-OSS Agent  
A standalone, cinematic agent built specifically for the **OpenAI Model Hackathon**.  
It recommends tools based on category, pricing, and feature filters using GPT-OSS.

---

## ⚒️ Tech Stack

### App
- **Frontend (Prototype):** Kodular (Phase 1 MVP)  
- **Frontend (Current):** Flutter  
- **Backend:** Flask (Replit + Render)  
- **CI/CD:** Manual APK signing + GitHub Actions  
- **OAuth2:** Discord + Google Suite integration

### Agent
- **Model:** TinyLlama/TinyLlama-1.1B-Chat-v1.0  
- **Libraries:** `transformers`, `torch`, `tqdm`, `requests`  
- **Execution:** Local run via `OneStackAI_Agent_GPT_OSS.py`  
- **Filtering:** Category, pricing, keyword, and feature toggles  
- **Fallback Logic:** Unicode-safe prompt handling + discoverability tagging

---

## 📁 Folder Structure
OneStackAI_OpenAI_Hackathon/ ├── OneStackAI_Agent_GPT_OSS.py ├── tools_query.py ├── tools.py ├── README.md ├── requirements.txt ├── install_log.txt ├──


---

## 🎥 Demo Highlights

- Agent runs independently from the app  
- HuggingChat surfaced organically via category + pricing filters  
- Fallback logic triggers when GPT-OSS fails silently  
- Output saved to `output.txt` for reproducibility  
- Install trace documented in `install_log.txt`

---

## 📦 App Features

- Unified dashboard for 100+ AI tools  
- Slash command support for real-time access  
- Dopamine-drop UX for neurodivergent clarity  
- QR-powered downloads for indie launches  
- Discord + Google Suite integration  
- Privacy-first routing (no data tracking)

---

## 🧠 Agent Highlights (Hackathon-Specific)

- Built fresh for OpenAI Model Hackathon  
- Modular, cinematic, and privacy-first  
- Tool recommendations based on real-time filters  
- HuggingChat tagged as a known OSS suggestion platform  
- Designed for indie developers and judge-grade clarity

---

## 💬 Community

Join the conversation via [Discord](https://discord.gg/KBstZbht) or [Telegram](https://t.me/OneStackAI)  
Submit feedback, suggest tools, or contribute.

---

## 🧠 Submission Context

Submitted to: **OpenAI Open Model Hackathon**  
Track: **Local Agent**  
Date: **Sept 1, 2025**  
Author: **Sunidhi Sourabh**  

---

## 🔮 Future Roadmap

- Merge agent into app backend  
- Add UI layer for tool recommendations  
- Upgrade tool source to dynamic API or SQLite  
- Fine-tune GPT-OSS for indie dev workflows

---

© 2025 Sunidhi Sourabh. All rights reserved.  
This repository and its contents are protected under applicable copyright laws.  
Unauthorized use, redistribution, or modification without explicit permission is prohibited.## 📁 Folder Structure
## 📁 Folder Structure
