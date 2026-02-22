# 🚀 CareerIQ — AI Career Advisor Chatbot

CareerIQ is a production-ready **AI-powered Career Advisor** built with **Streamlit** and **Google Gemini API**.  
It provides structured, expert-level guidance for career planning, resume review, job search strategy, and interview preparation.

This project demonstrates **real-world AI application design**, **prompt engineering**, **API integration**, and **cloud deployment on AWS EC2**.

---

## ✨ Key Features

- 🧭 **Career Path Planning** — step-by-step roadmaps
- 📄 **Resume & LinkedIn Review** — actionable, ATS-friendly feedback
- 🔍 **Skill Gap Analysis** — what to learn next & why
- 🎯 **Job Search Strategy** — platforms, outreach, and timelines
- 🎤 **Interview Preparation** — behavioral & role-based guidance
- 💬 **Salary Negotiation Advice** — communication frameworks
- 📎 **PDF Resume Upload (Optional)** — extract & analyze resume text
- ☁️ **Cloud Deployed** — running on AWS EC2

---

## 🧠 Tech Stack

| Layer | Technology |
|-----|-----------|
Frontend | Streamlit |
LLM | Google Gemini (`gemini-2.5-flash`) |
Backend | Python |
Prompt Control | Custom system prompt (career domain–restricted) |
PDF Parsing | `pdfplumber` |
Config Management | `python-dotenv` |
Logging | Python logging |
Deployment | AWS EC2 (Ubuntu) |

---

## 📂 Project Structure
# 🚀 CareerIQ — AI Career Advisor Chatbot

CareerIQ is a production-ready **AI-powered Career Advisor** built with **Streamlit** and **Google Gemini API**.  
It provides structured, expert-level guidance for career planning, resume review, job search strategy, and interview preparation.

This project demonstrates **real-world AI application design**, **prompt engineering**, **API integration**, and **cloud deployment on AWS EC2**.

---

## ✨ Key Features

- 🧭 **Career Path Planning** — step-by-step roadmaps
- 📄 **Resume & LinkedIn Review** — actionable, ATS-friendly feedback
- 🔍 **Skill Gap Analysis** — what to learn next & why
- 🎯 **Job Search Strategy** — platforms, outreach, and timelines
- 🎤 **Interview Preparation** — behavioral & role-based guidance
- 💬 **Salary Negotiation Advice** — communication frameworks
- 📎 **PDF Resume Upload (Optional)** — extract & analyze resume text
- ☁️ **Cloud Deployed** — running on AWS EC2

---

## 🧠 Tech Stack

| Layer | Technology |
|-----|-----------|
Frontend | Streamlit |
LLM | Google Gemini (`gemini-2.5-flash`) |
Backend | Python |
Prompt Control | Custom system prompt (career domain–restricted) |
PDF Parsing | `pdfplumber` |
Config Management | `python-dotenv` |
Logging | Python logging |
Deployment | AWS EC2 (Ubuntu) |

---

## 📂 Project Structure

```text
career-advisor-chatbot/
├── app.py                 # Streamlit UI
├── gemini_client.py       # Gemini API client
├── chat_manager.py        # Conversation memory
├── prompt_manager.py      # System & helper prompts
├── config.py              # Environment-based config
├── logger.py              # Centralized logging
├── requirements.txt
├── utils/
│   ├── __init__.py
│   └── pdf_utils.py       # PDF resume extraction
├── .env.example           # Sample environment variables
└── README.md

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/career-advisor-chatbot.git
cd career-advisor-chatbot

2️⃣ Create & activate virtual environment

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file:
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
TEMPERATURE=0.3
MAX_OUTPUT_TOKENS=2048
LOG_LEVEL=INFO

🔐 Never commit .env to GitHub.
5️⃣ Run the app

streamlit run app.py

☁️ Deployment on AWS EC2 (Ubuntu)
1️⃣ SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
2️⃣ Install system dependencies
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
3️⃣ Clone repo & setup
git clone https://github.com/<your-username>/career-advisor-chatbot.git
cd career-advisor-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
4️⃣ Add .env
nano .env
5️⃣ Run Streamlit
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

Access via browser:

http://<EC2_PUBLIC_IP>:8501

Ensure port 8501 is open in the EC2 security group.

🧩 Prompt Engineering (Core Design)

CareerIQ uses a strict system prompt to:

Stay 100% career-focused

Avoid hallucinated statistics

Provide structured, actionable advice

Enforce professional tone and guardrails

This makes responses feel expert-driven, not generic chatbot output.

🚫 Deliberate Limitations

No legal employment advice

No financial investment advice

No off-topic questions

No resume creation without user background

No fabricated job market data

These constraints improve trust and response quality.

🔮 Future Enhancements

Resume ↔ Job Description matching

Multi-user authentication

Conversation persistence (DB)

Voice interface

Analytics dashboard

Dockerized deployment

👩‍💻 Author

Revathy Gopinath
🔗 GitHub: https://github.com/revathygopinath

⭐ Why This Project Matters

This project demonstrates:

Real-world LLM integration

Clean architecture separation (UI / logic / prompts)

Cloud deployment skills

Strong product thinking

Responsible AI guardrails


