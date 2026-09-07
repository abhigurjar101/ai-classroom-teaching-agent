import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

# 1. Initialize the local LLM (using the Ollama setup we used earlier)
llm = ChatOllama(model="llama3", temperature=0.7)

# 2. Define the Teaching Persona
system_prompt = """You are an expert, patient, and encouraging tutor. 
Your goal is to help the student learn, NOT to just give them the answers.

Follow these rules:
1. Explain concepts simply and use analogies where helpful.
2. If the student asks how to solve a problem, guide them step-by-step instead of doing it for them.
3. Ask guiding questions to check their understanding.
4. Always be encouraging!"""

# 3. Create the Prompt Template with Memory capability
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 4. Chain them together
chain = prompt | llm

def start_tutoring_session():
    print("🎓 Teaching Agent initialized using Local Llama3! (Type 'quit' to exit)")
    print("-" * 60)
    
    chat_history = []
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nClass dismissed! Have a great day.")
                break
                
            print("\nTutor is thinking...")
            
            # 5. Generate the response
            response = chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            print(f"\n🎓 Tutor: {response.content}")
            print("-" * 60)
            
            # 6. Save the conversation history so the agent remembers context
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response.content))
            
        except KeyboardInterrupt:
            print("\nClass dismissed! Have a great day.")
            break
        except Exception as e:
            print(f"\nOops! Something went wrong: {e}")
            print("Make sure Ollama is running in the background!")
            break

if __name__ == "__main__":
    start_tutoring_session()
