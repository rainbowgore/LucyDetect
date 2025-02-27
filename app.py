import streamlit as st
import openai
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from drift_monitor import save_response_to_faiss, get_most_similar_response, calculate_similarity

# ✅ Load environment variables
load_dotenv()

# ✅ Backend API URL (FastAPI)
API_URL = "https://lucydetect.onrender.com"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Ensure API key is set
if not OPENAI_API_KEY:
    st.error("❌ ERROR: No OpenAI API Key found. Set OPENAI_API_KEY in .env")
    st.stop()

openai.api_key = OPENAI_API_KEY

# ✅ Streamlit UI
st.title("🔮 LLM Drift Analyzer")
query = st.text_input("Enter a prompt to analyze drift:")
submit_button = st.button("Analyze Drift")

def get_llm_response(query):
    """Fetch LLM response from OpenAI API."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": query}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ OpenAI API Error: {e}")
        return None

def analyze_drift(query):
    """Runs drift analysis on an LLM response and logs results."""
    timestamp = datetime.now().isoformat()

    # ✅ Get new response
    new_response = get_llm_response(query)
    if not new_response:
        return None

    st.write("### ✅ Latest Response:")
    st.write(new_response)

    # ✅ Compare with past responses
    save_response_to_faiss(new_response)
    past_response, similarity = get_most_similar_response(new_response)

    drift_score = 1 - similarity
    st.write(f"**📊 Similarity Score:** {similarity:.2f}")
    st.write(f"**⚠️ Drift Score:** {drift_score:.2f}")

    if drift_score > 0.3:
        st.warning("🚨 ALERT: High LLM drift detected!")

    # ✅ Store response using API
    payload = {
        "timestamp": timestamp,
        "query": query,
        "response": new_response,
        "similarity_score": float(similarity),  # 🔥 Fix float32 issue
        "drift_score": float(drift_score),      # 🔥 Fix float32 issue
    }
    api_response = requests.post(f"{API_URL}/save", json=payload)

    if api_response.status_code == 200:
        st.success("✅ Response saved successfully!")
    else:
        st.error(f"❌ Error saving response: {api_response.text}")

    return payload

def get_recent_responses():
    """Fetch recent responses from backend API."""
    response = requests.get(f"{API_URL}/recent")
    if response.status_code == 200:
        return response.json()
    st.error(f"❌ Error retrieving responses: {response.text}")
    return []

if submit_button and query:
    analyze_drift(query)

    # Fetch & display recent responses
    recent_responses = get_recent_responses()
    if recent_responses:
        st.write("### 🕒 Previous Responses:")
        for res in recent_responses:
            st.write(f"- **{res['timestamp']}**: {res['query']} → {res['response']}")