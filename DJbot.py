# app.py
# Import the required libraries
import streamlit as st # web interface for the chatbot.
from langchain_community.chat_models import ChatOllama # interface from LangChain’s community modules that connects to the Ollama models.
from langchain_core.output_parsers import StrOutputParser # Parses the language model’s output into a string
from langchain_core.prompts import ChatPromptTemplate # Helps structure the conversation prompt with system and human messages.
from langchain_core.messages import AIMessage, HumanMessage  # Custom message types to track messages from the AI and the user.

import streamlit as st # web interface for the chatbot.
from langchain_community.chat_models import ChatOllama # interface from LangChain’s community modules that connects to the Ollama models.
from langchain_core.output_parsers import StrOutputParser # Parses the language model’s output into a string
from langchain_core.prompts import ChatPromptTemplate # Helps structure the conversation prompt with system and human messages.
from langchain_core.messages import AIMessage, HumanMessage  # Custom message types to track messages from the AI and the user.

# Set page config
# Sets the title and icon shown in the browser tab. Layout is centered. 
# The sidebar is expanded by default.

st.set_page_config(
    page_title="Ask Me Anything Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ List of Models")
    model_size = st.radio(
        "Select Model :",
        ["DeepSeek-r1 1.5B", "Microsoft PHI3 14B"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("Steps to use:- ")
    st.markdown("a. Select the model")
    st.markdown("b. Type your question in the chat box")
    st.markdown("c. Press enter or click send")
    st.markdown("---")

# Model selection mapping
# Maps the human-readable model size options to the actual model identifiers used by the ChatOllama model. When a user selects a model size, the corresponding identifier is used in the chain.
model_map = {
    "DeepSeek-r1 1.5B": "deepseek-r1:1.5b",
    "PHI3 14B": "phi3:14b"
}

# Initialize LangChain components
def setup_chain(model_name):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Respond in a clear and concise manner."),
        ("human", "{input}")
    ])
    
    llm = ChatOllama(
        model=model_name,
        temperature=0.7,
        num_ctx=4096
    )
    
    return prompt | llm | StrOutputParser()


# Main chat interface
st.title("💬 Ask Me Anything Chatbot")
st.caption("🚀 A local AI chatbot powered by latest LLM models")

# Initialize session state for messages
# This ensures that the chat history (the list of messages) persists between interactions. If there’s no existing message history, an empty list is initialized.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("ai"):
            st.markdown(message.content)

# User input handling
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Display user message
    with st.chat_message("human"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("ai"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Get selected model
        selected_model = model_map[model_size]
        
        # Initialize chain
        chain = setup_chain(selected_model)
        
        # Stream response
        for chunk in chain.stream({"input": prompt}):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    # Add AI response to chat history
    st.session_state.messages.append(AIMessage(content=full_response))