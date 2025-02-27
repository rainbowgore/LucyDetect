import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LOG_FILE = "logs.json"

# Load embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Initialize FAISS Index
dimension = 384
index = faiss.IndexFlatL2(dimension)

def save_response_to_faiss(response):
    """Convert response to embedding & store in FAISS"""
    vector = embedding_model.encode([response])
    index.add(np.array(vector))

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append({"response": response})

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def get_most_similar_response(new_response, lookback=5):
    """Find the closest past response in FAISS within the last N responses"""
    vector = embedding_model.encode([new_response])
    _, idx = index.search(np.array(vector), lookback)

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    if logs:
        similarities = []
        for i in idx[0]:
            past_response = logs[i]["response"]
            similarity = calculate_similarity(past_response, new_response)
            similarities.append((past_response, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[0]

    return None, 0

def calculate_similarity(text1, text2):
    """Compute cosine similarity between two text embeddings"""
    vector1 = embedding_model.encode([text1])
    vector2 = embedding_model.encode([text2])
    return cosine_similarity(vector1, vector2)[0][0]