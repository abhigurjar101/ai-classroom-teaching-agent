# AI classroom teaching agent

A local tutoring prototype that connects Streamlit and LangChain prompts to Ollama's `llama3` model. It demonstrates guided questioning and separate student and teacher views, reflecting my AI/ML training and mentorship work.

## Setup

```bash
git clone https://github.com/abhigurjar101/ai-classroom-teaching-agent.git
cd ai-classroom-teaching-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3
# Keep Ollama running in a separate terminal if the desktop service is not running:
# ollama serve
streamlit run classroom_app.py
```

Install Ollama separately before pulling the model. Model downloads require network access, disk space, and suitable hardware. For a terminal session, run `python teaching_agent.py`. `app.py` is an alternate single-page UI.

## Demonstration flow

Use a fictional learner name, ask a Python or ML question, then open the teacher view to inspect the saved conversation and ask for teaching advice. The prompt asks the model to guide learning; it cannot guarantee that the model will withhold answers or teach correctly.

## Data and limitations

`classroom_app.py` writes learner names, timestamps, and full messages to `student_logs.json`. The teacher view has no authentication or role-based authorization. Local JSON writes do not support concurrent classroom sessions safely. This is a local demonstration, not a privacy-preserving production classroom system. Use synthetic conversations and add authorization, consent, retention controls, and session isolation before using real learner data.

The dashboard displays conversation history and model-generated advice. It does not calculate validated comprehension milestones or learning outcomes. No educational-effectiveness result is claimed.

## Repository map

- `teaching_agent.py`: CLI with conversation history
- `classroom_app.py`: student chat, JSON logs, teacher advice
- `app.py`: alternate tutor UI
- `requirements.txt`: application dependencies

[Abhi Kumar Gurjar](https://www.linkedin.com/in/abhigurjar)
