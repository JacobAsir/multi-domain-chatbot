import streamlit as st
from langchain.llms import HuggingFaceEndpoint
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(
    page_title="💬 Domain-Specific Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Instructions
st.sidebar.title("🤖 Domain-Specific Chatbot")
st.sidebar.write("""
This chatbot assists with queries in **Healthcare**, **Insurance**, **Finance**, and **Retail**.
Out-of-domain queries will receive a standard response.
""")

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0  # For usage analytics

@st.cache_resource
def load_llm():
    hf_api_key = os.getenv("HF_TOKEN")
    if not hf_api_key:
        st.error("Hugging Face API token not found. Please set it in the environment variables.")
        st.stop()
    
    repo_id = "jacobasir/MultiDomainChatbot"  
    try:
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            huggingfacehub_api_token=hf_api_key,
            max_length=150,
            temperature=0.7
        )
        return llm
    except Exception as e:
        st.error(f"Error loading HuggingFaceEndpoint: {e}")
        st.stop()

llm = load_llm()

# Function to classify domains
def classify_domain(query):
    healthcare_keywords = ["symptom", "disease", "medicine", "treatment", "appointment"]
    insurance_keywords = ["policy", "claim", "coverage", "premium", "insurance"]
    finance_keywords = ["investment", "loan", "credit", "finance", "bank"]
    retail_keywords = ["product", "price", "order", "retail", "availability"]

    if any(keyword in query.lower() for keyword in healthcare_keywords):
        return "Healthcare"
    elif any(keyword in query.lower() for keyword in insurance_keywords):
        return "Insurance"
    elif any(keyword in query.lower() for keyword in finance_keywords):
        return "Finance"
    elif any(keyword in query.lower() for keyword in retail_keywords):
        return "Retail"
    else:
        return "Out-of-Domain"


# Function to generate chatbot response
def generate_response(user_query):
    domain = classify_domain(user_query)
    if domain == "Out-of-Domain":
        return "I can only assist with queries related to Healthcare, Insurance, Finance, or Retail."
    
    system_prompt = f"""
You are a helpful assistant specializing in the {domain} domain.
Please provide accurate, context-specific answers based on user queries.
"""
    full_prompt = system_prompt + f"\nUser: {user_query}\nAnswer:"
    
    try:
        response = llm(full_prompt)
        return response.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Chat interface
st.title("💬 Domain-Specific Chatbot")

# Display chat history
for chat in st.session_state.history:
    if chat['role'] == 'user':
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Chatbot:** {chat['message']}")

# User input
user_input = st.text_input("You:", key="input", placeholder="Type your query here...")

# Handle Send button
if st.button("Send") and user_input:
    with st.spinner("Chatbot is typing..."):
        response = generate_response(user_input)
        
        st.session_state.history.append({"role": "user", "message": user_input})
        st.session_state.history.append({"role": "bot", "message": response})
        
        st.session_state.query_count += 1  # Increment query count
        st.experimental_rerun()

# Optional: Analytics and Chat History Download
if st.sidebar.button("Download Chat Log"):
    chat_log = pd.DataFrame(st.session_state.history)
    chat_log.to_csv("chat_log.csv", index=False)
    st.sidebar.success("Chat log saved as 'chat_log.csv'.")

# Chatbot usage analytics
st.sidebar.write("### Usage Analytics")
st.sidebar.write(f"Total Queries: {st.session_state.query_count}")
