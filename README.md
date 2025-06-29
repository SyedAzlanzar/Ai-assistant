# AI Writing Assistant

An intelligent assistant that crafts cover letters and responses with user-selected tone. Built using the OpenAI API, JWT authentication, and MongoDB for storage.

---

## 🚀 Features

- **User authentication** with JWT (signup/login).
- **AI chat assistant** powered by OpenAI (**gpt‑3.5‑turbo** or **gpt‑4**, as configured).
- **Role- & tone-based generation** (e.g., student, HR; professional, friendly).
- **Cover letter PDF export**, formatted with:
  - **Bold name**
  - 📍 *address*
  - 📞 *phone with icon* alongside email
  - Extracted subject line based on job description
  - Tailored body and sign-off
- **PDF generation** using FPDF with Unicode-capable fonts.

---

## 🛠️ Tech Stack

**Backend**  
- Python, FastAPI  
- OpenAI API for AI-powered responses  
- JWT auth for secure sessions  
- MongoDB for user data storage  
- PDF generation using FPDF (supports custom fonts and structured layout)

**Frontend (planned)**  
- React (Vite) or Next.js Chrome extension:
  - Register / Login / Forgot Password  
  - AI Assistant tab with tone control  
  - Cover Letter export to PDF using onboarded user info

---

## ⚙️ Getting Started

### 1. Clone and setup

```bash
git clone https://github.com/your_username/ai-writing-assistant.git
cd ai-writing-assistant
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```


### 2. Configure .env

```bash
MONGO_URI=<your-mongodb-uri>
SECRET_KEY=<your-jwt-secret>
OPENAI_API_KEY=<optional-openai-key>
```

### 3. Start Server

```bash
uvicorn app.main:app --reload
```




