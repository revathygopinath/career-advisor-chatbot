# 🚀 CareerIQ — AI Career Advisor

CareerIQ is a **production-ready AI Career Advisor** built with **Streamlit** and **Google Gemini**.  
It helps users with **career guidance, resume reviews, job search strategies, and career transitions**, including **PDF resume upload and analysis**.

🌐 **Live App:**  
👉 http://18.188.93.72:8501

---

## ✨ Features

- 🤖 AI-powered career guidance using **Google Gemini**
- 📄 Resume review (text + PDF upload support)
- 🧭 Career path planning & skill-gap analysis
- 🎯 Job search & interview preparation guidance
- 💬 Conversational memory for context-aware responses
- 🧱 Modular, production-grade architecture
- ☁️ Deployed on **AWS EC2 (Ubuntu)**

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **LLM:** Google Gemini (gemini-2.5-flash)
- **Backend:** Python 3.10+
- **PDF Parsing:** pdfplumber
- **Config Management:** python-dotenv
- **Deployment:** AWS EC2 (Ubuntu 22.04)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
career-advisor-chatbot/
│
├── app.py                 # Streamlit UI
├── gemini_client.py       # Gemini API client
├── chat_manager.py        # Conversation memory
├── prompt_manager.py      # System & helper prompts
├── config.py              # Environment-based config
├── logger.py              # Centralized logging
├── requirements.txt       # Python dependencies
│
├── utils/
│   ├── __init__.py
│   └── pdf_utils.py       # PDF resume extraction
│
├── .env.example           # Sample environment variables
├── README.md



⚙️ Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
TEMPERATURE=0.3
MAX_OUTPUT_TOKENS=512
LOG_LEVEL=INFO
🧑‍💻 Local Setup
# Clone repository
git clone https://github.com/revathygopinath/career-advisor-chatbot.git
cd career-advisor-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

Open:

http://localhost:8501
☁️ Deployment on AWS EC2
# SSH into EC2
ssh -i careeriq-key.pem ubuntu@<EC2_PUBLIC_IP>

# Navigate to project
cd career-advisor-chatbot
source venv/bin/activate

# Run Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

Access the app:

http://<EC2_PUBLIC_IP>:8501
🔄 Keep App Running After Logout
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
🎯 Use Cases

Final-year students exploring career options

Career switchers moving into Data / Tech roles

Resume optimization & ATS-friendly feedback

Interview preparation & skill roadmap planning

📌 Future Improvements

🔐 Authentication

🌍 Custom domain + HTTPS

📊 Usage analytics

🗂 Resume version comparison

🧠 Long-term user memory

👩‍💻 Author

Revathy Gopinath
Data Scientist | AI & Analytics Enthusiast

🔗 GitHub: https://github.com/revathygopinath

🔗 LinkedIn: https://linkedin.com/in/revathy-gopinath