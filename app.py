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
    raise ValueError("❌ ERROR: No OpenAI API Key found. Set OPENAI_API_KEY in .env")

openai.api_key = OPENAI_API_KEY

def get_llm_response(query):
    """Fetch LLM response from OpenAI API."""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        temperature=0.7
    )
    return response.choices[0].message.content

def analyze_drift(query):
    """Runs drift analysis on an LLM response and logs results."""
    timestamp = datetime.now().isoformat()

    # ✅ Get new response
    new_response = get_llm_response(query)
    print(f"New Response: {new_response}")

    # ✅ Compare with past responses
    save_response_to_faiss(new_response)
    past_response, similarity = get_most_similar_response(new_response)

    drift_score = 1 - similarity
    print(f"Similarity Score: {similarity:.2f}")
    print(f"Drift Score: {drift_score:.2f}")

    if drift_score > 0.3:
        print("🚨 ALERT: High LLM drift detected!")

    # ✅ Store response using API
    payload = {
        "timestamp": timestamp,
        "query": query,
        "response": new_response,
        "similarity_score": similarity,
        "drift_score": drift_score,
    }
    api_response = requests.post(f"{API_URL}/save", json=payload)

    if api_response.status_code == 200:
        print("✅ Response saved successfully!")
    else:
        print(f"❌ Error saving response: {api_response.text}")

    return payload

def get_recent_responses():
    """Fetch recent responses from backend API."""
    response = requests.get(f"{API_URL}/recent")
    if response.status_code == 200:
        return response.json()
    print(f"❌ Error retrieving responses: {response.text}")
    return []

if __name__ == "__main__":
    # Example run
    query = "Explain why LLMs experience model drift."
    analyze_drift(query)

    # Fetch & print recent responses
    recent_responses = get_recent_responses()
    print("Recent Responses:", recent_responses)