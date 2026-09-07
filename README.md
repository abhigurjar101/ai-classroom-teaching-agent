# AI Classroom & Socratic Teaching Agent 👨‍🏫🎓

> **An autonomous Socratic AI tutoring and classroom telemetry system built with LangChain, Local Ollama (Llama 3), and Streamlit by Abhi Gurjar.**

---

## 💡 What Is This Project? (Explained Like a Human)

When students use typical AI chatbots for homework, they usually copy-paste the problem and the AI immediately gives them the finished answer. The student gets an A on the homework, but when the real exam comes, they haven't learned anything because their brain never did the work.

**This project implements a Socratic AI Teaching Agent.**
- Instead of handing out raw answers, the agent acts like a master tutor: it breaks complex problems down, uses relatable real-world analogies, and asks guiding questions that encourage the student to discover the solution on their own.
- **Dual-Portal Architecture**:
  1. **Student Help Portal**: An encouraging, interactive interface where students can ask questions about Python, Math, Data Science, or Machine Learning at any time of day.
  2. **Teacher Analytics Dashboard**: Gives educators real-time telemetry on student confusion hotspots, session durations, and comprehension milestones without violating student privacy.
- **100% Local & Private**: Runs on-device via **Ollama (Llama 3)**, ensuring zero data leakage and zero recurring cloud API bills.

---

## 🏛️ System Architecture

```
[ Student Portal (Streamlit) ] ──► [ LangChain Conversational Memory ]
                                                 │
                                                 ▼
                                     [ Socratic Prompt Chain ]
                                                 │
                                                 ▼
                                      [ Local Ollama Llama 3 ]
                                                 │
                                                 ▼
[ Teacher Dashboard ] ◄────── [ Telemetry & Session Logger (JSON) ]
```

---

## 🚀 How to Run in 5 Seconds

```bash
# 1. Clone the repository
git clone https://github.com/abhigurjar101/ai-classroom-teaching-agent.git
cd ai-classroom-teaching-agent

# 2. Run CLI Tutoring Session
python3 teaching_agent.py

# 3. Or launch the full dual-portal Streamlit web app
streamlit run classroom_app.py
```

---

## 📁 Repository Structure

```
ai-classroom-teaching-agent/
├── classroom_app.py    # Streamlit dual-portal web app (Student Portal + Teacher Dashboard)
├── teaching_agent.py   # CLI Socratic tutoring session with LangChain memory
├── app.py              # Single-page tutor launcher
├── student_logs.json   # Session telemetry and comprehension logs
├── requirements.txt    # LangChain, Ollama, Streamlit dependencies
└── README.md           # You are here! Simple human documentation
```

---

## 👤 Author

**Abhi Gurjar**  
- Portfolio: [abhigurjar.vercel.app](https://abhigurjar.vercel.app)  
- GitHub: [@abhigurjar101](https://github.com/abhigurjar101)  
- LinkedIn: [Abhi Gurjar](https://in.linkedin.com/in/abhi-gurjar-b13067203)
