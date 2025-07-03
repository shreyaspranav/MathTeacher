import streamlit as st
from datetime import datetime
import time
import dotenv

from math_agent import MathAgent

# Load the API Keys
dotenv.load_dotenv()

# Initialize the Math Agent
agent = MathAgent(test=1)
agent.build_graph()

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

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## Chat with your AI Math Tutor")

with col2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Math Tutor. Ask me any mathematics question and I'll help you solve it step by step!"}
        ]
        st.rerun()

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_ai_response(user_input):
    
    response = agent.app.invoke({'query': user_input})
    print(f'Final Response: {response['solution']}')
    return response['solution']

# Chat input
if prompt := st.chat_input("Ask me a math question... (e.g., 'Solve x² + 5x + 6 = 0')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.markdown("# Math Tutor.")
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
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Generate response
            response = get_ai_response(question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    st.markdown("---")

    sample_jee_advanced_questions = [
        "Let $S$ be the set of all complex numbers $Z$ satisfying $|z-2+i| \\geq \\sqrt{5}$. If the complex number $Z_{0}$ is such that $\\frac{1}{\\left|Z_{0}-1\\right|}$ is the maximum of the set $\\left\\{\\frac{1}{|z-1|}: z \\in S\\right\\}$, then the principal argument of $\\frac{4-z_{0}-\\overline{z_{0}}}{Z_{0}-\\overline{z_{0}}+2 i}$ is\n\n(A) $-\\frac{\\pi}{2}$\n\n(B) $\\frac{\\pi}{4}$\n\n(C) $\\frac{\\pi}{2}$\n\n(D) $\\frac{3 \\pi}{4}$",
        "Let $\\alpha, \\beta, \\gamma, \\delta$ be real numbers such that $\\alpha^{2}+\\beta^{2}+\\gamma^{2} \\neq 0$ and $\\alpha+\\gamma=1$. Suppose the point $(3,2,-1)$ is the mirror image of the point $(1,0,-1)$ with respect to the plane $\\alpha x+\\beta y+\\gamma z=\\delta$. Then which of the following statements is/are TRUE?\n\n(A) $\\alpha+\\beta=2$\n\n(B) $\\delta-\\gamma=3$\n\n(C) $\\delta+\\beta=4$\n\n(D) $\\alpha+\\beta+\\gamma=\\delta$",
        "If $f(x)=\\left|\\begin{array}{ccc}\\cos (2 x) & \\cos (2 x) & \\sin (2 x) \\\\ -\\cos x & \\cos x & -\\sin x \\\\ \\sin x & \\sin x & \\cos x\\end{array}\\right|$, then\n\n[A] $f^{\\prime}(x)=0$ at exactly three points in $(-\\pi, \\pi)$\n\n[B] $f^{\\prime}(x)=0$ at more than three points in $(-\\pi, \\pi)$\n\n[C] $f(x)$ attains its maximum at $x=0$\n\n[D] $f(x)$ attains its minimum at $x=0$",
        "Consider the hyperbola\n\n\\[\n\\frac{x^{2}}{100}-\\frac{y^{2}}{64}=1\n\\]\n\nwith foci at $S$ and $S_{1}$, where $S$ lies on the positive $x$-axis. Let $P$ be a point on the hyperbola, in the first quadrant. Let $\\angle S P S_{1}=\\alpha$, with $\\alpha<\\frac{\\pi}{2}$. The straight line passing through the point $S$ and having the same slope as that of the tangent at $P$ to the hyperbola, intersects the straight line $S_{1} P$ at $P_{1}$. Let $\\delta$ be the distance of $P$ from the straight line $S P_{1}$, and $\\beta=S_{1} P$. Then what is the greatest integer less than or equal to $\\frac{\\beta \\delta}{9} \\sin \\frac{\\alpha}{2}$?",
        "Consider an obtuse angled triangle $A B C$ in which the difference between the largest and the smallest angle is $\\frac{\\pi}{2}$ and whose sides are in arithmetic progression. Suppose that the vertices of this triangle lie on a circle of radius 1. Then what is the inradius of the triangle ABC?"
    ]
    
    st.header("JEE Advanced Math Questions")
    for i in range(len(sample_jee_advanced_questions)):
        if st.button(f'Question {i + 1}', key=f"sample_{sample_jee_advanced_questions[i][:10]}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": sample_jee_advanced_questions[i]})
            
            # Generate response
            response = get_ai_response(sample_jee_advanced_questions[i])
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    st.markdown("---")