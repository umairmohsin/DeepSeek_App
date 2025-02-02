import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS styling
st.markdown("""
<style>
    /* Existing styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("DeepSeek Code Collaborater 🧠")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 🐍 Python Expert
    - 🐞 Debugging Assistant
    - 📝 Code Documentation
    - 💡 Solution Design
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

#Chat engine 
llm = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.3,
    format=""  # or "" for plain text
)

system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide only concise and correct solutions "
    "with strategic print statements for debugging. Always respond in English. And if you dont know the answer just tell can't figure it out but dont give incorrect response"
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? 💻"}]


chat_container = st.container()

with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.write(message["content"])

#use chat input and processing
user_query = st.chat_input("Type your message here...")

def gen_ai(prompt_chain):
    processing = prompt_chain | llm | StrOutputParser()
    return processing.invoke({})

def build_prompt_chain():
    prompt_seq = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_seq.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_seq.append(AIMessagePromptTemplate.from_template(msg["content"]))
    
    return ChatPromptTemplate.from_messages(prompt_seq)  # Use from_messages instead of from_template


if user_query:
    #Add to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    with st.spinner("Thinking..."):
        prompt_chain = build_prompt_chain()
        ai_response = gen_ai(prompt_chain)
    
    st.session_state.message_log.append({"role":"ai" , "content":ai_response})
    
    #Dsiplay on frontend
    
    st.rerun()