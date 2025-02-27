from fastapi import FastAPI
import os
from database import save_response, get_latest_responses  # Ensure database.py exists
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LucyDetect Backend Running"}

@app.post("/save")
def save_data(data: dict):
    save_response(
        data["timestamp"], data["query"], data["response"], 
        data["similarity_score"], data["drift_score"]
    )
    return {"status": "saved"}

@app.get("/recent")
def get_data():
    return get_latest_responses()