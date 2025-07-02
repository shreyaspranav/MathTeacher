import streamlit as st
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="AI Math Tutor",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI Math Tutor. Ask me any mathematics question and I'll help you solve it step by step!"}
    ]

# Create two columns for layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## Chat with your AI Math Tutor")

with col2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Math Tutor. Ask me any mathematics question and I'll help you solve it step by step!"}
        ]
        st.rerun()

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Mock AI response function (replace this with your actual AI logic)
def get_ai_response(user_input):
    """
    Mock function that echoes back the user input
    Replace this with your actual AI processing logic
    """
    # Simulate processing time
    time.sleep(0.5)
    
    # For now, just echo back the input with some formatting
    response = f"""
        **You asked:** {user_input}

        **AI Response:** I received your question: "{user_input}"
        
        This is a test response
    """
    return response

# Chat input
if prompt := st.chat_input("Ask me a math question... (e.g., 'Solve x² + 5x + 6 = 0')"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with additional features
with st.sidebar:
    st.markdown("# Math Tutor.")
    st.markdown("---")

    st.header("Chat Stats")
    
    # Calculate stats
    total_messages = len(st.session_state.messages)
    user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
    
    st.metric("Total Messages", total_messages)
    st.metric("Your Questions", user_messages)
    
    st.markdown("---")
    
    st.header("Sample Questions")
    sample_questions = [
        "Solve x² + 5x + 6 = 0",
        "Find the derivative of f(x) = 3x³",
        "What is the area of a triangle?",
        "Explain the quadratic formula",
        "How do I factor polynomials?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=f"sample_{question[:10]}", use_container_width=True):
            # Add the sample question as if user typed it
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Generate response
            response = get_ai_response(question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    st.markdown("---")
    
    st.header("About")
    st.info("""
    This is a demo interface for the Math Routing Agent.
    
    **Features:**
    - Real-time chat interface
    - Message history
    - Sample questions
    - Chat statistics
    """)