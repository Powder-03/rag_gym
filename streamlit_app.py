"""
GymPro RAG Chatbot - Streamlit Frontend
"""
import streamlit as st
import requests
import json
import os
from typing import Dict, Any
import time

# Page configuration
st.set_page_config(
    page_title="GymPro AI Assistant",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        display: flex;
        flex-direction: column;
        color: #212529;
        font-size: 1rem;
        line-height: 1.5;
    }
    .user-message {
        background-color: #FFFFFF;
        border-left: 4px solid #2196F3;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .assistant-message {
        background-color: #FFFFFF;
        border-left: 4px solid #FF6B35;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .source-box {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 0.3rem;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.8rem;
        color: #495057;
    }
    .status-indicator {
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-healthy {
        background-color: #C8E6C9;
        color: #2E7D32;
    }
    .status-unhealthy {
        background-color: #FFCDD2;
        color: #C62828;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

def check_api_health() -> Dict[str, Any]:
    """Check if the API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return {
            "healthy": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {
            "healthy": False,
            "error": str(e)
        }

def send_chat_message(message: str) -> Dict[str, Any]:
    """Send a message to the chatbot API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None,
            "error": response.text if response.status_code != 200 else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_api_status() -> Dict[str, Any]:
    """Get detailed API status"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return {
            "success": response.status_code == 200,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    # Header
    st.markdown('<h1 class="main-header">🏋️ GymPro AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### Your Personal Fitness & Gym Expert")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 System Status")
        
        # Health check
        health_status = check_api_health()
        if health_status["healthy"]:
            st.markdown('<div class="status-indicator status-healthy">✅ API Healthy</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-unhealthy">❌ API Unavailable</div>', 
                       unsafe_allow_html=True)
            st.error(f"Error: {health_status.get('error', 'Unknown error')}")
        
        # Detailed status
        with st.expander("📊 Detailed Status"):
            api_status = get_api_status()
            if api_status["success"] and api_status["data"]:
                status_data = api_status["data"]
                st.json(status_data)
            else:
                st.error("Unable to fetch detailed status")
        
        st.divider()
        
        # Instructions
        st.header("💡 How to Use")
        st.markdown("""
        **Ask me about:**
        - Exercise techniques & form
        - Workout routines & programs
        - Gym equipment usage
        - Nutrition & supplements
        - Injury prevention
        - Bodybuilding & powerlifting
        
        **Example questions:**
        - "How do I perform a proper deadlift?"
        - "What's a good chest workout routine?"
        - "How much protein should I eat?"
        """)
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm GymPro AI, your personal fitness assistant. I'm here to help you with workout routines, exercise techniques, nutrition advice, and everything gym-related. What would you like to know?",
            "sources": []
        })

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🧑 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🏋️ GymPro AI:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Display sources if available
            if message.get("sources") and len(message["sources"]) > 0:
                st.markdown("**📚 Sources:**")
                for i, source in enumerate(message["sources"][:3], 1):
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {i}:</strong> {source}
                    </div>
                    """, unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask me anything about fitness, workouts, or gym-related topics..."):
        # Check API health before sending
        if not check_api_health()["healthy"]:
            st.error("⚠️ API is currently unavailable. Please check if the backend service is running.")
            return
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑 You:</strong><br>
            {prompt}
        </div>
        """, unsafe_allow_html=True)
        
        # Show thinking spinner
        with st.spinner("🤔 GymPro AI is thinking..."):
            # Send message to API
            response = send_chat_message(prompt)
            
            if response["success"] and response["data"]:
                data = response["data"]
                assistant_message = data.get("response", "Sorry, I couldn't generate a response.")
                sources = data.get("sources", [])
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message,
                    "sources": sources
                })
                
            else:
                error_msg = "Sorry, I encountered an error while processing your request."
                if response.get("error"):
                    error_msg += f" Error: {response['error']}"
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": []
                })
        
        # Rerun to show the new message
        st.rerun()

    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🏋️ GymPro AI**")
    with col2:
        st.markdown("*Powered by RAG & Google AI*")
    with col3:
        if st.button("📖 API Docs"):
            st.link_button("Open API Documentation", f"{API_BASE_URL}/docs")

if __name__ == "__main__":
    main()
