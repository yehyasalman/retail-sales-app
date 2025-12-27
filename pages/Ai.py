import streamlit as st
from google import genai
import pandas as pd

# 1. API Configuration
# Note: In a real project, use st.secrets for your API key!
API_KEY = "AIzaSyAORjfxuka1FCEgZlxMyG0HDIytesPyoqw"
client = genai.Client(api_key=API_KEY)

import streamlit as st
from google import genai

innovators_academy_info = pd.read_csv("retail_store_sales.csv")

st.title("🤖 Innovators Academy AI")

# 2. INITIALIZATION with the correct "parts" and "text" structure
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user", 
            "parts": [{"text": innovators_academy_info}]
        },
        {
            "role": "model", 
            "parts": [{"text": "Hello! I am the Innovators Academy assistant. How can I help you today?"}]
        }
    ]

# 3. DISPLAY HISTORY
for msg in st.session_state.messages:
    # Skip the background context
    if innovators_academy_info in msg["parts"][0]["text"]:
        continue
    
    with st.chat_message(msg["role"]):
        # Note the nested access: msg["parts"][0]["text"]
        st.markdown(msg["parts"][0]["text"])

# 4. USER INPUT
if prompt := st.chat_input("Ask something..."):
    # Add user message using the correct structure
    user_msg = {"role": "user", "parts": [{"text": prompt}]}
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. GENERATE RESPONSE
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Now contents=st.session_state.messages will work perfectly!
        stream = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=st.session_state.messages,
        )

        for chunk in stream:
            full_response += chunk.text
            response_placeholder.markdown(full_response)
        
        response_placeholder.markdown(full_response)
    
    # Save the assistant response
    st.session_state.messages.append({
        "role": "model", 
        "parts": [{"text": full_response}]
    })
