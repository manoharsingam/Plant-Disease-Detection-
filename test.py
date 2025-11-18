import os
import io
import sqlite3
import threading
import numpy as np
import json
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

# ---------------------------
# CONFIG
# ---------------------------
MODEL_PATH = "model/perfect_fit_final.h5"
DB_PATH = "users.db"
IMG_SIZE = (300, 300)
GEMINI_API_KEY = "AIzaSyCyWF6GaRIXOKVBXONnQAm69DJm1OmmqTk"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

CLASS_NAMES = [
"Pepper__bell___Bacterial_spot",
"Pepper__bell___healthy",
"Potato___Early_blight",
"Potato___Late_blight",
"Potato___healthy",
"Tomato_Bacterial_spot",
"Tomato_Early_blight",
"Tomato_Late_blight",
"Tomato_Leaf_Mold",
"Tomato_Septoria_leaf_spot",
"Tomato_Spider_mites_Two_spotted_spider_mite",
"Tomato__Target_Spot",
"Tomato__Tomato_YellowLeaf__Curl_Virus",
"Tomato__Tomato_mosaic_virus",
"Tomato_healthy"
]


# ---------------------------
# FLASK APP
# ---------------------------
app = Flask(__name__)

# ---------------------------
# DATABASE INIT
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# ROUTES: HTML PAGES
# ---------------------------
@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/home")
def home_page():
    return render_template("home.html")

# ---------------------------
# SIGNUP API
# ---------------------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hashed))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or Email already exists"}), 409

    return jsonify({"success": True})

# ---------------------------
# LOGIN API
# ---------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "User not found"}), 404

    username, hashed_pw = row

    if not check_password_hash(hashed_pw, password):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"success": True, "username": username})

# ---------------------------
# MODEL LOADING
# ---------------------------
model = load_model(MODEL_PATH, compile=False)
predict_lock = threading.Lock()

# ---------------------------
# GEMINI AI HELPER
# ---------------------------
def get_gemini_recommendations(disease_label, confidence):
    """Get fertilizer recommendations, severity, and pesticide locations using Gemini AI"""
    
    # Clean up disease label
    clean_disease = disease_label.replace("_", " ").replace("  ", " - ")
    
    prompt = f"""You are an expert agricultural pathologist analyzing plant diseases.

DISEASE DETECTED: {clean_disease}
CONFIDENCE: {confidence*100:.2f}%

Provide detailed agricultural recommendations. Respond with ONLY a valid JSON object (no markdown, no explanation, just pure JSON):

{{
  "severity": "mild/moderate/severe",
  "severity_description": "2-3 sentences explaining the severity and impact",
  "fertilizer_recommendations": [
    "Specific NPK fertilizer with ratio for {clean_disease}",
    "Micronutrient recommendation for this disease",
    "Organic amendment to boost plant immunity"
  ],
  "treatment_steps": [
    "Immediate action with specific fungicide/pesticide name for {clean_disease}",
    "Application method and frequency",
    "Cultural practice to prevent spread",
    "Monitoring and follow-up actions"
  ],
  "pesticide_shops_hyderabad": [
    {{"name": "Kaveri Seeds", "area": "Secunderabad", "contact": "040-27803456"}},
    {{"name": "Nagarjuna Agrichem", "area": "Kukatpally", "contact": "040-23456789"}},
    {{"name": "Coromandel Fertilizers", "area": "Somajiguda", "contact": "040-23401234"}},
    {{"name": "Rallis India Limited", "area": "Begumpet", "contact": "9876543210"}},
    {{"name": "UPL Limited", "area": "Tarnaka", "contact": "Visit for details"}}
  ],
  "prevention_tips": [
    "Specific prevention for {clean_disease}",
    "Environmental management tip",
    "Crop rotation or resistant variety advice"
  ]
}}

Guidelines:
- For Tomato Leaf Mold: moderate-severe, fungicides like Mancozeb/Chlorothalonil, reduce humidity
- For Tomato Blight (Early/Late): severe, copper-based fungicides, remove infected parts immediately
- For Spider Mites: mild-moderate, miticides/acaricides, increase humidity
- For Bacterial Spot: moderate, copper bactericides, avoid overhead watering
- For Viral Diseases: severe, no cure exists, remove and destroy infected plants
- For Septoria Leaf Spot: moderate, fungicides, remove lower leaves
- For Target Spot: moderate, fungicides with chlorothalonil
- For Healthy Plants: mild, preventive care only

Make ALL recommendations highly specific to {clean_disease}."""

    print(f"\n{'='*60}")
    print(f"🔍 CALLING GEMINI API FOR: {clean_disease}")
    print(f"{'='*60}\n")
    
    # Prepare request payload
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    try:
        # Make API request
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ API Error Response:")
            print(response.text)
            raise Exception(f"Gemini API returned status {response.status_code}: {response.text}")
        
        # Parse response
        result = response.json()
        
        print("\n📩 GEMINI RAW RESPONSE:")
        print("-" * 60)
        print(json.dumps(result, indent=2))
        print("-" * 60)
        
        # Extract text from response
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                response_text = candidate["content"]["parts"][0]["text"].strip()
                
                print("\n📝 EXTRACTED TEXT:")
                print(response_text[:500])
                print("...")
                
                # Clean up response - remove markdown code blocks
                if "```json" in response_text:
                    response_text = response_text.split("```json", 1)[1].split("```", 1)[0]
                elif "```" in response_text:
                    parts = response_text.split("```")
                    if len(parts) >= 3:
                        response_text = parts[1]
                    elif len(parts) == 2:
                        response_text = parts[1]
                
                response_text = response_text.strip()
                
                # Parse JSON
                recommendations = json.loads(response_text)
                
                print("\n✅ PARSED JSON SUCCESSFULLY!")
                print(json.dumps(recommendations, indent=2))
                print(f"\n{'='*60}\n")
                
                return recommendations
        
        raise Exception("No valid content in Gemini response")
        
    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT ERROR: Gemini API took too long to respond")
        print(f"{'='*60}\n")
        raise Exception("API Timeout - Please try again")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ REQUEST ERROR: {str(e)}")
        print(f"{'='*60}\n")
        raise Exception(f"Network error: {str(e)}")
        
    except json.JSONDecodeError as je:
        print(f"\n❌ JSON DECODE ERROR: {str(je)}")
        try:
            print(f"Attempted to parse: {response_text[:500]}...")
        except:
            print("Could not print response text")
        print(f"{'='*60}\n")
        raise Exception(f"Invalid JSON from Gemini: {str(je)}")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise

def get_fallback_recommendations(disease_label):
    """This function should NEVER be called - always raise error instead"""
    raise Exception("CRITICAL: Fallback was called - this should never happen!")

# ---------------------------
# IMAGE PROCESSING HELPERS
# ---------------------------
def read_imagefile(file_bytes):
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img).astype("float32")
    arr = np.expand_dims(arr, 0)
    return preprocess_input(arr)

def top_k(probs, k=3):
    probs = probs.flatten()
    idx = probs.argsort()[-k:][::-1]
    return [(i, float(probs[i])) for i in idx]

# ---------------------------
# PREDICT API
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file sent"}), 400

    img_bytes = request.files["file"].read()
    x = read_imagefile(img_bytes)

    with predict_lock:
        preds = model.predict(x)[0]

    top3 = top_k(preds)
    label = CLASS_NAMES[top3[0][0]]
    conf = top3[0][1]

    print(f"\n{'='*60}")
    print(f"DISEASE DETECTED: {label}")
    print(f"CONFIDENCE: {conf*100:.2f}%")
    print(f"{'='*60}\n")

    # Get AI-powered recommendations (MUST succeed - no fallback allowed)
    try:
        print("🤖 Calling Gemini API for AI-generated recommendations...")
        print("⚠️  NO FALLBACK MODE - API MUST SUCCEED")
        gemini_data = get_gemini_recommendations(label, conf)
        
        # Verify we got valid AI response
        if not gemini_data or not isinstance(gemini_data, dict):
            raise Exception("Gemini returned invalid data structure")
        
        # Verify all required fields exist
        required_fields = ["severity", "severity_description", "fertilizer_recommendations", 
                          "treatment_steps", "pesticide_shops_hyderabad", "prevention_tips"]
        missing = [f for f in required_fields if f not in gemini_data]
        if missing:
            raise Exception(f"Gemini response missing fields: {missing}")
        
        result = {
            "label": label,
            "confidence": conf,
            "top3": [{"label": CLASS_NAMES[i], "confidence": c} for i, c in top3],
            "severity": gemini_data["severity"],
            "severity_description": gemini_data["severity_description"],
            "fertilizer_recommendations": gemini_data["fertilizer_recommendations"],
            "treatment_steps": gemini_data["treatment_steps"],
            "pesticide_shops_hyderabad": gemini_data["pesticide_shops_hyderabad"],
            "prevention_tips": gemini_data["prevention_tips"],
            "notes": "✅ 100% AI-Generated Analysis (Gemini Pro)",
            "ai_source": "Google Gemini Pro"
        }
        
        print("\n✅ SUCCESS: FINAL AI-GENERATED RESULT:")
        print(json.dumps(result, indent=2))
        print(f"\n{'='*60}\n")
        
        return jsonify(result)
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ CRITICAL FAILURE: Gemini API did not provide valid response")
        print(f"Error: {error_msg}")
        print(f"{'='*60}\n")
        
        # Return error - NO fallback recommendations
        return jsonify({
            "error": f"AI Analysis Failed: {error_msg}. Please try again or check API status.",
            "error_type": "GEMINI_API_FAILURE",
            "label": label,
            "confidence": conf,
            "top3": [{"label": CLASS_NAMES[i], "confidence": c} for i, c in top3],
            "message": "No pre-written fallback available. Only AI-generated responses are used."
        }), 500

# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)