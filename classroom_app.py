import streamlit as st
import json
import os
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# File to store student logs
LOG_FILE = "student_logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_log(student_name, role, content):
    logs = load_logs()
    if student_name not in logs:
        logs[student_name] = []
    
    logs[student_name].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "content": content
    })
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# Setup page
st.set_page_config(page_title="AI Classroom", page_icon="🏫", layout="wide")
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select View:", ["👨‍🎓 Student Portal", "👨‍🏫 Teacher Dashboard"])

# Initialize Local LLM
llm = ChatOllama(model="llama3", temperature=0.7)

if app_mode == "👨‍🎓 Student Portal":
    st.title("👨‍🎓 Student Help Portal")
    st.write("Welcome! I'm your AI Tutor. Ask me any question about what you're learning today.")
    
    student_name = st.text_input("Please enter your name to begin:")
    
    if student_name:
        if "student_chat" not in st.session_state:
            st.session_state.student_chat = []
            
        # Student Prompt
        tutor_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a patient, encouraging tutor. Do not give direct answers. Guide the student step-by-step. Ask guiding questions to check understanding."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        tutor_chain = tutor_prompt | llm
        
        # Display history
        for msg in st.session_state.student_chat:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            with st.chat_message(role):
                st.write(msg.content)
                
        # Chat input
        if user_input := st.chat_input(f"What do you need help with, {student_name}?"):
            with st.chat_message("user"):
                st.write(user_input)
            
            save_log(student_name, "student", user_input)
            
            with st.chat_message("assistant"):
                with st.spinner("Tutor is thinking..."):
                    response = tutor_chain.invoke({
                        "input": user_input,
                        "chat_history": st.session_state.student_chat
                    })
                    st.write(response.content)
            
            save_log(student_name, "tutor", response.content)
            
            st.session_state.student_chat.append(HumanMessage(content=user_input))
            st.session_state.student_chat.append(AIMessage(content=response.content))

elif app_mode == "👨‍🏫 Teacher Dashboard":
    st.title("👨‍🏫 Teacher Dashboard")
    st.write("Monitor student progress and get AI advice on how to help them.")
    
    logs = load_logs()
    
    if not logs:
        st.info("No students have used the tutor yet.")
    else:
        # Select a student to review
        selected_student = st.selectbox("Select a student to review their chat:", list(logs.keys()))
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"{selected_student}'s Chat History")
            student_history = logs[selected_student]
            
            # Format history as a string for the AI
            history_text = ""
            with st.container(height=400):
                for entry in student_history:
                    if entry['role'] == 'student':
                        st.markdown(f"**{selected_student}:** {entry['content']}")
                        history_text += f"Student: {entry['content']}\n"
                    else:
                        st.markdown(f"**Tutor:** {entry['content']}")
                        history_text += f"Tutor: {entry['content']}\n"
        
        with col2:
            st.subheader("🤖 Teacher's Assistant")
            st.write("Ask the AI for advice on how to help this student based on their chat history.")
            
            if "teacher_chat" not in st.session_state:
                st.session_state.teacher_chat = []
                
            teacher_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert Teacher's Assistant. Your job is to help the human teacher. "
                           "Review the student's chat history below and give pedagogical advice, pinpoint "
                           "where the student is confused, or help draft a lesson plan. \n\n"
                           "STUDENT CHAT HISTORY:\n{history}\n\n"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])
            teacher_chain = teacher_prompt | llm
            
            # Display teacher chat
            for msg in st.session_state.teacher_chat:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                with st.chat_message(role):
                    st.write(msg.content)
                    
            if teacher_input := st.chat_input("Ask for teaching advice regarding this student..."):
                with st.chat_message("user"):
                    st.write(teacher_input)
                
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing student history..."):
                        response = teacher_chain.invoke({
                            "history": history_text,
                            "input": teacher_input,
                            "chat_history": st.session_state.teacher_chat
                        })
                        st.write(response.content)
                
                st.session_state.teacher_chat.append(HumanMessage(content=teacher_input))
                st.session_state.teacher_chat.append(AIMessage(content=response.content))
