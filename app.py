import streamlit as st
import tempfile
import os

from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

st.set_page_config(page_title="Teaching Agent", page_icon="🎓", layout="wide")
st.title("🎓 AI Teaching Agent")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Sidebar for file upload
with st.sidebar:
    st.header("📚 Course Material")
    uploaded_file = st.file_uploader("Upload a file to learn about", type=['pdf', 'txt', 'csv'])
    
    if uploaded_file and st.session_state.vectorstore is None:
        with st.spinner("Reading and processing file..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Load Document
            if uploaded_file.name.endswith('.pdf'):
                loader = PyPDFLoader(tmp_path)
            elif uploaded_file.name.endswith('.csv'):
                loader = CSVLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path)
                
            docs = loader.load()
            
            # Chunking
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            
            # Embeddings & Vectorstore
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(splits, embeddings)
            st.session_state.vectorstore = vectorstore
            
            st.success("File processed! You can now ask questions.")

# Set up the LLM
llm = ChatOllama(model="llama3", temperature=0.7)

# Teaching Persona Prompt
system_prompt = """You are an expert, patient, and encouraging tutor. 
Your goal is to help the student learn the material from the provided context, NOT to just give them the answers.

Rules:
1. Use the provided context to answer the student's questions.
2. Explain concepts simply and use analogies where helpful.
3. If the student asks how to solve a problem, guide them step-by-step.
4. Ask guiding questions to check their understanding.
5. If the answer is not in the context, say so, but try to guide them conceptually if possible.

Context:
{context}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Display chat history
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.write(msg.content)

# Chat input
if user_input := st.chat_input("Ask me a question about your file..."):
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Tutor is thinking..."):
            if st.session_state.vectorstore:
                # RAG chain
                retriever = st.session_state.vectorstore.as_retriever()
                
                # Contextualize question (simple version for this UI)
                question_answer_chain = create_stuff_documents_chain(llm, prompt)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)
                
                response = rag_chain.invoke({
                    "input": user_input,
                    "chat_history": st.session_state.chat_history
                })
                answer = response["answer"]
            else:
                # Normal chat (no file uploaded)
                normal_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful tutor. Please remind the user to upload a document in the sidebar to learn specific material, but answer their general question anyway."),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{input}")
                ])
                chain = normal_prompt | llm
                response = chain.invoke({
                    "input": user_input,
                    "chat_history": st.session_state.chat_history
                })
                answer = response.content
                
            st.write(answer)
            
    # Update history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=answer))
