from fastapi import FastAPI
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# ✅ Connect to MongoDB safely
db, collection = None, None  # Initialize as None
if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        db = client["lucydetect"]
        if db is not None:  # ✅ Explicitly check for None
            collection = db["responses"]
        print("✅ MongoDB connection works!")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LucyDetect Backend Running"}

@app.post("/save")
def save_data(data: dict):
    if collection is None:
        return {"error": "No database connection"}
    
    collection.insert_one({
        "timestamp": data["timestamp"],
        "query": data["query"],
        "response": data["response"],
        "similarity_score": data["similarity_score"],
        "drift_score": data["drift_score"]
    })
    return {"status": "saved"}

@app.get("/recent")
def get_data():
    if collection is None:
        return {"error": "No database connection"}
    streamlit run app.py
    return list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(5))