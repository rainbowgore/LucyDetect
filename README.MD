# 🔮 LucyDetect - LLM Drift Analyzer

## 📌 Overview

LucyDetect helps developers and AI researchers analyze **LLM response drift** over time. It tracks and compares responses from **GPT models**, measuring consistency and detecting unexpected changes.

## Why Does This Matter? (Industry Gap)

### 🔍 **The Problem: No Standard for Monitoring LLM Consistency**
Right now, AI teams, researchers, and businesses have **no standard way** to:
1. **Detect when an LLM response changes over time**.
2. **Measure how different two LLM-generated answers are**.
3. **Track drift after fine-tuning, retraining, or updates**.
4. **Compare two LLM models (e.g., GPT-4o vs. GPT-3.5) for reliability**.
5. **Prevent AI hallucinations and ensure factual consistency**.

### 🛠 **How LucyDetect Fills the Gap**
LucyDetect **quantifies response drift** by:
✔ **Logging** all GPT responses in a database.  
✔ **Using FAISS for similarity search** to compare past answers.  
✔ **Computing drift scores** based on semantic similarity.  
✔ **Visualizing trends** over time with an interactive UI.  

---

## 🚀 Features

✅ **Detect Response Drift** → Compare past and current LLM outputs.  
✅ **Log & Analyze Trends** → Track drift scores over time.  
✅ **Store & Retrieve Data** → Securely save responses for future comparison.  
✅ **Custom API Key Support** → Users enter their own OpenAI API key.  
✅ **Web UI (Streamlit)** → Easy-to-use interface for drift detection.  

---

## 🔹 **Use Cases**

### 👩‍💻 **For AI Developers**
- **Monitor model consistency** across deployments.  
- **Detect drift** when fine-tuning or retraining LLMs.  
- **Benchmark different OpenAI models** before production use.  

### 🏢 **For Businesses**
- Ensure **AI-generated responses stay consistent** for users.  
- Prevent **sudden answer changes in customer-facing applications**.  

### 🔬 **For Researchers**
- Study **long-term model behavior** under different conditions.  
- Investigate **semantic drift in language models over time**.  

---

## 🔹 **How to Use LucyDetect**

### 1️⃣ **Use the Public Web UI (No Installation Required)**
_Anyone can use LucyDetect online without setup!_  
🔗 **[LucyDetect Web UI](https://your-streamlit-app-link)**  

---

### 2️⃣ **Run Locally (For Developers)**
**Clone the repo and install dependencies:**
```bash
git clone https://github.com/your-repo/lucydetect.git
cd lucydetect
pip install -r requirements.txt