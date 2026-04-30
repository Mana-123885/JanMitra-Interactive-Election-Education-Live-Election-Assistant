# JanMitra — जनमित्र
### "Mera Chunav, Meri Awaaz" (My Election, My Voice)

JanMitra is a modern, gamified educational platform designed to empower Indian citizens with accurate knowledge about the democratic process. It transforms complex election procedures into an engaging learning journey.

---

## 🏛️ Chosen Vertical: Civic Tech & Election Education
JanMitra focuses on **Civic Literacy**. In a country as large as India, understanding the electoral process—from voter registration to VVPAT verification—is crucial for a healthy democracy. This app addresses the gap between official data and public awareness using interactive technology.

## 🧠 Approach and Logic

### 1. Gamified Learning Path
The application is built on a **progression-based logic**. Users don't just read facts; they embark on a "Civic Hero" journey. 
- **XP (Experience Points)**: Earned through learning modules, quizzes, and debunking myths.
- **Dynamic Levels**: Users progress through 8 distinct levels (e.g., Nagarika Seedha to Democracy Champion).
- **Badge Engine**: A backend service monitors 20 different achievement criteria to award visual badges.

### 2. Information Architecture
The solution uses a **modular web-based architecture**:
- **Core Layer**: Manages shared services like the database (SQLite), navigation, and multi-language support.
- **Data Layer**: Centralized JSON repositories for verified election facts, ensuring 100% accuracy and easy updates.
- **UI Layer**: A premium, responsive web interface built with HTML5, CSS3, and JavaScript, served via a Flask backend. This ensures compatibility with any browser and cloud environments like Google Cloud Shell.

## 🚀 How the Solution Works

- **Interactive Process Map**: A 12-stage curriculum that breaks down the election cycle into digestible steps.
- **Polling Day Simulator**: A first-person simulation that prepares voters for the physical experience at the booth, including queue rules and EVM usage.
- **Civic Assistant (Chatbot)**: A keyword-driven AI that provides instant answers to frequently asked questions about ECI rules and procedures.
- **Myth vs Fact**: An interactive module where users "reveal" the truth behind common election misconceptions, earning rewards for their curiosity.
- **Live Tracker**: Fetches real-time news updates via RSS feeds to provide structured information on historical and upcoming election phases.

## 📝 Assumptions Made

1.  **Authorized Content**: All educational content is assumed to be derived from the Election Commission of India (ECI) and the Constitution of India.
2.  **Hybrid Access**: While the core suite is local for fast performance, the app can fetch live news when internet is available.
3.  **Target Audience**: Designed for both first-time voters (18-21) needing basic guidance and experienced voters looking to deepen their civic knowledge.
4.  **Cloud & Browser Ready**: Optimized for deployment on platforms like Google Cloud Shell and accessible via any modern web browser.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.10+ with Flask
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), JavaScript (SPA Architecture)
- **Database**: SQLite3 (Local persistence)
- **APIs/Services**: Feedparser (Live News), Flask-CORS

## 📦 Installation & Setup
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the application:
   ```bash
   python main.py
   ```
5. **Access the App**:
   - On Local: Open `http://127.0.0.1:8080` in your browser.
   - On Google Cloud Shell: Click **Web Preview** -> **Preview on port 8080**.

---

*Disclaimer: JanMitra is a non-partisan educational tool. It is not affiliated with any political party.*
