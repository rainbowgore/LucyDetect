import asyncio
import streamlit as st
import openai
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# ✅ Fix for "RuntimeError: no running event loop" in Python 3.12+
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# ✅ Load environment variables
load_dotenv()

# ✅ Backend API URL
API_URL = "https://lucydetect.onrender.com"  # Change to your actual backend URL
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Ensure API key is set
if not OPENAI_API_KEY:
    st.error("❌ ERROR: No OpenAI API Key found. Set OPENAI_API_KEY in Streamlit Secrets.")
    st.stop()

openai.api_key = OPENAI_API_KEY

# ✅ Streamlit UI
st.title("🔮 LLM Drift Analyzer")
openai_api_key = st.text_input("🔑 Enter Your OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("⚠️ Please enter an OpenAI API key.")
    st.stop()
openai.api_key = openai_api_key

query = st.text_input("Enter your prompt:")
submit_button = st.button("Analyze Drift")

def get_llm_response(query):
    """Fetch LLM response from OpenAI API."""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        temperature=0.7
    )
    return response.choices[0].message.content

if submit_button and query:
    timestamp = datetime.now().isoformat()

    # ✅ Get new response from OpenAI
    new_response = get_llm_response(query)
    st.write("### ✅ Latest Response:")
    st.write(new_response)

    # ✅ Send to backend for drift analysis
    payload = {
        "timestamp": timestamp,
        "query": query,
        "response": new_response,
        "similarity_score": 0.0,  # Placeholder (backend computes actual similarity)
        "drift_score": 0.0,  # Placeholder
    }
    response = requests.post(f"{API_URL}/save", json=payload)

    if response.status_code == 200:
        st.success("✅ Response saved successfully!")
    else:
        st.error(f"❌ Error saving response: {response.text}")

    # ✅ Retrieve past responses from backend
    response = requests.get(f"{API_URL}/recent")
    if response.status_code == 200:
        recent_responses = response.json()
        if recent_responses:
            st.write("### 🕒 Previous Responses:")
            for res in recent_responses:
                st.write(f"- **{res['timestamp']}**: {res['query']} → {res['response']}")
    else:
        st.error(f"❌ Error fetching recent responses: {response.text}")