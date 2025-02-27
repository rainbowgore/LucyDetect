from fastapi import FastAPI, HTTPException
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "lucydetect")  # Default database name

# ✅ Ensure MongoDB URI is set
if not MONGO_URI:
    raise ValueError("❌ ERROR: No MongoDB URI found. Set MONGO_URI in Render Secrets.")

try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client[DB_NAME]
    collection = db["responses"]
    client.admin.command('ping')  # ✅ Check if MongoDB is reachable
    print("✅ Connected to MongoDB!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    collection = None

# ✅ Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    """Health check endpoint."""
    return {"message": "Backend is running!"}

@app.post("/save")
def save_data(data: dict):
    """Save LLM response to MongoDB."""
    if not collection:
        raise HTTPException(status_code=500, detail="❌ Database connection failed.")

    try:
        collection.insert_one(data)
        return {"status": "✅ Saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error saving data: {str(e)}")

@app.get("/recent")
def get_recent_responses(limit: int = 5):
    """Fetch recent LLM responses from MongoDB."""
    if not collection:
        raise HTTPException(status_code=500, detail="❌ Database connection failed.")

    try:
        recent_responses = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
        return recent_responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error fetching data: {str(e)}")

# ✅ Run test if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)