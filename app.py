import openai
import os
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from drift_monitor import save_response_to_faiss, get_most_similar_response, calculate_similarity

# ✅ Load environment variables
load_dotenv()

# ✅ Backend API URL (FastAPI on Render)
API_URL = os.getenv("API_URL")  # Set this in Streamlit Secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in Streamlit Secrets

# ✅ Ensure API key is set
if not OPENAI_API_KEY:
    st.error("❌ ERROR: No OpenAI API Key found. Set OPENAI_API_KEY in Streamlit Secrets.")
    st.stop()

openai.api_key = OPENAI_API_KEY

# ✅ Streamlit UI
st.title("🔮 LLM Drift Analyzer")
st.write("Compare AI responses over time to detect inconsistencies.")

# ✅ User input
query = st.text_input("Enter your prompt:")
submit_button = st.button("Analyze Drift")

# ✅ Function to get response from OpenAI
def get_llm_response(query):
    """Fetch LLM response from OpenAI API."""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ✅ Function to analyze drift
def analyze_drift(query):
    """Runs drift analysis and logs results via the backend API."""
    timestamp = datetime.now().isoformat()

    # ✅ Get new response from OpenAI
    new_response = get_llm_response(query)

    # ✅ Compare with past responses
    save_response_to_faiss(new_response)
    past_response, similarity = get_most_similar_response(new_response)

    drift_score = 1 - similarity  # Higher = more drift

    # ✅ Display drift scores
    st.write("### ✅ Latest Response:")
    st.write(new_response)
    st.write(f"**📊 Similarity Score:** {similarity:.2f}")
    st.write(f"**⚠️ Drift Score:** {drift_score:.2f}")

    if drift_score > 0.3:
        st.warning("🚨 ALERT: High LLM drift detected!")

    # ✅ Store response via backend API
    payload = {
        "timestamp": timestamp,
        "query": query,
        "response": new_response,
        "similarity_score": similarity,
        "drift_score": drift_score,
    }
    api_response = requests.post(f"{API_URL}/save", json=payload)

    if api_response.status_code == 200:
        st.success("✅ Response saved successfully!")
    else:
        st.error(f"❌ Error saving response: {api_response.text}")

    return payload

# ✅ Fetch recent responses
def get_recent_responses():
    """Fetch recent responses from backend API."""
    response = requests.get(f"{API_URL}/recent")
    if response.status_code == 200:
        return response.json()
    st.error(f"❌ Error retrieving responses: {response.text}")
    return []

# ✅ Main execution
if submit_button and query:
    analyze_drift(query)

    # ✅ Fetch & display recent responses
    recent_responses = get_recent_responses()
    if recent_responses:
        st.write("### 🕒 Previous Responses:")
        for res in recent_responses:
            st.write(f"- **{res['timestamp']}**: {res['query']} → {res['response']}")