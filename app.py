import os
import io
import sqlite3
import threading
import numpy as np
import requests
import google.generativeai as genai

from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

# --------------- Basic Config ----------------
MODEL_PATH = "model/perfect_fit_final.h5"
DB_PATH = "users.db"
IMG_SIZE = (300, 300)

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
    "Tomato_healthy",
]

# --------------- API Key for Gemini ----------------
GEMINI_API_KEY ="Your gemini api key"

# Initialize Gemini only if API key is available
gemini_model = None
gemini_available = False

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Try to list available models first
        try:
            available = list(genai.list_models())
            print(f"Found {len(available)} available models")
            
            # Find models that support generateContent
            for m in available:
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name.replace('models/', '')
                    try:
                        gemini_model = genai.GenerativeModel(model_name)
                        # Quick test
                        test_response = gemini_model.generate_content("Hi")
                        gemini_available = True
                        print(f"✓ Gemini API initialized successfully with model: {model_name}")
                        break
                    except:
                        continue
        except Exception as list_error:
            print(f"Could not list models: {str(list_error)[:100]}")
            
            # Fallback: try common model names without 'models/' prefix
            model_names = [
                "gemini-1.5-flash-001",
                "gemini-1.5-pro-001",
                "gemini-1.0-pro",
                "gemini-pro",
                "models/gemini-1.5-flash",
                "models/gemini-pro"
            ]
            
            for model_name in model_names:
                try:
                    gemini_model = genai.GenerativeModel(model_name)
                    test_response = gemini_model.generate_content("Hi")
                    gemini_available = True
                    print(f"✓ Gemini API initialized successfully with model: {model_name}")
                    break
                except Exception as model_error:
                    continue
        
        if not gemini_available:
            print("✗ No working Gemini model found")
            print("  Your API key might be invalid or expired")
            print("  Get a new key from: https://aistudio.google.com/app/apikey")
            
    except Exception as e:
        print(f"✗ Gemini API initialization failed: {str(e)}")
        gemini_available = False
else:
    print("⚠ GEMINI_API_KEY not found in environment variables")
    print("  Set it using: export GEMINI_API_KEY=your_key_here")

# --------------- Flask Setup ----------------
app = Flask(__name__)

# --------------- Database Init ----------------
def init_db():
    try:
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
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {str(e)}")

init_db()

# --------------- Render HTML Routes ----------------
@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/home")
def home_page():
    return render_template("home.html")

# --------------- Signup API ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hashed_pw))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True})
        
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 409
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({"error": "An error occurred during signup"}), 500

# --------------- Login API ----------------
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing fields"}), 400

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
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"error": "An error occurred during login"}), 500

# --------------- Load Model ----------------
try:
    model = load_model(MODEL_PATH, compile=False)
    predict_lock = threading.Lock()
    print("✓ ML Model loaded successfully")
except Exception as e:
    print(f"✗ Model loading failed: {str(e)}")
    print(f"  Make sure '{MODEL_PATH}' exists")
    model = None

# --------------- Image Preprocessing ----------------
def read_imagefile(file_bytes):
    try:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img = img.resize(IMG_SIZE)
        arr = np.array(img).astype("float32")
        arr = np.expand_dims(arr, 0)
        return preprocess_input(arr)
    except Exception as e:
        print(f"Image preprocessing error: {str(e)}")
        raise

# --------------- Fallback Recommendations ----------------
FALLBACK_RECOMMENDATIONS = {
    "Pepper__bell___Bacterial_spot": """
• **Disease**: Bacterial spot causes dark spots on leaves and fruits, reducing yield quality.
• **Organic Treatment**: Remove infected leaves, spray with copper-based organic fungicide or neem oil.
• **Chemical Treatment**: Apply copper hydroxide or streptomycin sulfate as per label instructions.
• **Prevention**: Use disease-free seeds, avoid overhead watering, maintain proper plant spacing for air circulation.
""",
    "Potato___Early_blight": """
• **Disease**: Early blight causes dark brown spots on older leaves, leading to defoliation.
• **Organic Treatment**: Remove affected leaves, spray with Bacillus subtilis or copper fungicides.
• **Chemical Treatment**: Apply chlorothalonil or mancozeb fungicides every 7-10 days.
• **Prevention**: Practice crop rotation, avoid wetting foliage, use resistant varieties.
""",
    "Potato___Late_blight": """
• **Disease**: Late blight causes water-soaked lesions on leaves and tubers, can destroy entire crops quickly.
• **Organic Treatment**: Remove infected plants immediately, spray copper fungicides preventively.
• **Chemical Treatment**: Apply metalaxyl, chlorothalonil, or mancozeb at first signs.
• **Prevention**: Plant certified disease-free seeds, ensure good drainage, avoid overhead irrigation.
""",
    "Tomato_Bacterial_spot": """
• **Disease**: Bacterial spot causes small dark spots on leaves and fruits, reducing marketability.
• **Organic Treatment**: Spray copper-based fungicides or biological controls like Bacillus.
• **Chemical Treatment**: Use copper hydroxide or copper sulfate as preventive spray.
• **Prevention**: Use disease-free transplants, practice crop rotation, avoid working with wet plants.
""",
    "Tomato_Early_blight": """
• **Disease**: Early blight creates concentric ring patterns on lower leaves, causing yellowing and drop.
• **Organic Treatment**: Prune affected leaves, apply neem oil or baking soda solution (1 tbsp/liter).
• **Chemical Treatment**: Spray with chlorothalonil or mancozeb fungicides weekly.
• **Prevention**: Mulch around plants, water at base, maintain 2-year crop rotation.
""",
    "Tomato_Late_blight": """
• **Disease**: Late blight causes rapid browning and death of leaves and fruits, especially in humid weather.
• **Organic Treatment**: Remove infected parts immediately, spray copper fungicides preventively.
• **Chemical Treatment**: Apply metalaxyl-M or dimethomorph at first symptom.
• **Prevention**: Improve air circulation, avoid overhead watering, use resistant varieties like Mountain Magic.
""",
    "Tomato_Leaf_Mold": """
• **Disease**: Leaf mold causes yellow patches on upper leaf surface with olive-green mold below.
• **Organic Treatment**: Increase ventilation, spray with sulfur or copper fungicides.
• **Chemical Treatment**: Use chlorothalonil or mancozeb, ensure good greenhouse ventilation.
• **Prevention**: Reduce humidity below 85%, prune for airflow, use resistant hybrids.
""",
    "Tomato_Septoria_leaf_spot": """
• **Disease**: Septoria causes small circular spots with gray centers on lower leaves first.
• **Organic Treatment**: Remove infected leaves, spray with copper fungicide or neem oil.
• **Chemical Treatment**: Apply chlorothalonil or mancozeb every 7-10 days.
• **Prevention**: Mulch to prevent soil splash, water at base, practice 3-year crop rotation.
""",
    "Tomato_Spider_mites_Two_spotted_spider_mite": """
• **Disease**: Spider mites cause yellow stippling on leaves and fine webbing, weakening plants.
• **Organic Treatment**: Spray with strong water jet, apply neem oil or insecticidal soap.
• **Chemical Treatment**: Use abamectin or spiromesifen, rotate products to prevent resistance.
• **Prevention**: Monitor regularly, maintain humidity, introduce predatory mites like Phytoseiulus.
""",
    "Tomato__Target_Spot": """
• **Disease**: Target spot creates concentric ring lesions on leaves, stems, and fruits.
• **Organic Treatment**: Remove infected plant parts, apply copper fungicides or biological controls.
• **Chemical Treatment**: Spray with chlorothalonil or azoxystrobin.
• **Prevention**: Improve air circulation, avoid leaf wetness, use resistant varieties.
""",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": """
• **Disease**: Viral disease causing upward leaf curling, yellowing, and stunted growth.
• **Organic Treatment**: No cure - remove infected plants, control whitefly vectors with neem oil.
• **Chemical Treatment**: Use imidacloprid or thiamethoxam to control whitefly populations.
• **Prevention**: Use virus-free transplants, install yellow sticky traps, plant resistant varieties like Tyking.
""",
    "Tomato__Tomato_mosaic_virus": """
• **Disease**: Viral infection causing mottled light and dark green patterns on leaves.
• **Organic Treatment**: No cure - remove infected plants immediately to prevent spread.
• **Chemical Treatment**: No chemical cure available, focus on sanitation and prevention.
• **Prevention**: Disinfect tools with 10% bleach, wash hands after handling tobacco, use resistant varieties.
""",
    "healthy": """
• **Status**: Your plant appears healthy! Continue good practices.
• **Maintenance**: Water regularly at base, ensure 6-8 hours sunlight, apply balanced fertilizer monthly.
• **Monitoring**: Check weekly for pests or disease signs on undersides of leaves.
• **Prevention**: Maintain proper spacing, prune dead leaves, practice crop rotation annually.
"""
}

# --------------- Gemini Recommendation ----------------
def generate_ai_recommendation(disease_label: str):
    # Try Gemini API first
    if gemini_available and gemini_model:
        prompt = f"""
You are an agriculture expert in India. Disease detected: {disease_label}.

Write 4–6 short bullet points:
1. Simple explanation of the disease.
2. Natural/organic treatment options.
3. Chemical treatment (only generic names, with proper safety warnings).
4. Preventive methods for future.

Use simple English, bullet points, and no long paragraphs.
"""
        try:
            response = gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            print("Falling back to local recommendations...")
    
    # Fallback to local recommendations
    for key in FALLBACK_RECOMMENDATIONS:
        if key.lower() in disease_label.lower():
            return FALLBACK_RECOMMENDATIONS[key]
    
    # Check if healthy
    if "healthy" in disease_label.lower():
        return FALLBACK_RECOMMENDATIONS["healthy"]
    
    # Generic fallback
    return """
• **Disease Detected**: Please consult with a local agriculture expert for specific treatment.
• **General Care**: Remove affected leaves, ensure proper watering and sunlight.
• **Monitoring**: Check plants daily for any changes in symptoms.
• **Expert Help**: Contact your nearest agriculture extension office for personalized advice.
"""

# --------------- Predict API ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded. Please check server logs."}), 500
        
        if "file" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        image_bytes = file.read()
        
        # Validate image
        if len(image_bytes) == 0:
            return jsonify({"error": "Empty file uploaded"}), 400
        
        img_arr = read_imagefile(image_bytes)

        with predict_lock:
            predictions = model.predict(img_arr)[0]

        index = int(np.argmax(predictions))
        disease_label = CLASS_NAMES[index]
        confidence = float(predictions[index])

        recommendation = generate_ai_recommendation(disease_label)

        return jsonify({
            "label": disease_label,
            "confidence": confidence,
            "ai_recommendation": recommendation,
            "gemini_used": gemini_available
        })
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# --------------- Health Check API ----------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "gemini_available": gemini_available,
        "database_ok": os.path.exists(DB_PATH)
    })

# --------------- List Available Gemini Models ----------------
@app.route("/api/list-models", methods=["GET"])
def list_models():
    if not GEMINI_API_KEY:
        return jsonify({"error": "No API key configured"}), 400
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models = genai.list_models()
        available_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                available_models.append({
                    "name": m.name,
                    "display_name": m.display_name,
                    "description": m.description
                })
        return jsonify({"models": available_models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------- Run Server ----------------
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Plant Disease Detection System")
    print("="*50)
    print(f"Model loaded: {'✓' if model else '✗'}")
    print(f"Gemini API: {'✓' if gemini_available else '✗ (using fallback recommendations)'}")
    print(f"Database: {'✓' if os.path.exists(DB_PATH) else '✗'}")
    print("="*50 + "\n")
    
    if not gemini_available:
        print("⚠ To enable Gemini AI recommendations:")
        print("  1. Get API key from: https://aistudio.google.com/app/apikey")
        print("  2. Set environment variable:")
        print("     export GEMINI_API_KEY=your_key_here")
        print("  3. Restart the application\n")
    
    app.run(port=5000, debug=True)