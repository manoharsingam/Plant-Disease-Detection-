import os
import io
import sqlite3
import threading
import numpy as np
import requests
import google.generativeai as genai
import cv2

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

# --------------- Pesticide Stores in Hyderabad ----------------
# Bing Maps search link for pesticide stores in Hyderabad
PESTICIDE_STORES_SEARCH_LINK = "https://www.bing.com/maps?q=pesticide+stores+in+hyderabad"

# --------------- API Key for Gemini ----------------
GEMINI_API_KEY = ""
gemini_model = None
gemini_available = False

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        try:
            available = list(genai.list_models())
            for m in available:
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name.replace('models/', '')
                    try:
                        gemini_model = genai.GenerativeModel(model_name)
                        gemini_model.generate_content("Hi")
                        gemini_available = True
                        break
                    except:
                        continue
        except:
            model_names = [
                "gemini-1.5-flash-001",
                "gemini-1.5-pro-001",
                "gemini-pro",
            ]
            for model_name in model_names:
                try:
                    gemini_model = genai.GenerativeModel(model_name)
                    gemini_model.generate_content("Hi")
                    gemini_available = True
                    break
                except:
                    continue
    except:
        gemini_available = False

# --------------- Flask Setup ----------------
app = Flask(__name__)

# --------------- Database Init ----------------
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

@app.route("/store")
def store_page():
    return render_template("store.html")

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
    except:
        return jsonify({"error": "Signup failed"}), 500

# --------------- Login API ----------------
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT username, password FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        username, hashed_pw = user

        if not check_password_hash(hashed_pw, password):
            return jsonify({"error": "Incorrect password"}), 401

        return jsonify({"success": True, "username": username})

    except:
        return jsonify({"error": "Login failed"}), 500

# --------------- Load Model ----------------
try:
    model = load_model(MODEL_PATH, compile=False)
    predict_lock = threading.Lock()
except:
    model = None

# --------------- Image Preprocessing ----------------
def read_imagefile(file_bytes):
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img).astype("float32")
    arr = np.expand_dims(arr, 0)
    return preprocess_input(arr)

# --------------- LEAF DETECTION ----------------
def is_leaf_image(img_arr):
    """Rejects non-leaf images."""
    img = img_arr[0]
    img_uint8 = img.astype("uint8")

    hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV)

    # Green range
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / (img.shape[0] * img.shape[1])

    # Threshold: at least 25% should be green
    return green_ratio > 0.25

# --------------- Structured Disease Information ----------------
DISEASE_INFO = {
    "Pepper__bell___Bacterial_spot": {
        "disease_name": "Bacterial Spot",
        "plant_type": "Bell Pepper",
        "severity": "Medium",
        "symptoms": [
            "Small, dark brown spots on leaves",
            "Yellow halo around spots",
            "Spots on fruits and stems",
            "Defoliation in severe cases"
        ],
        "causes": [
            "Xanthomonas bacteria",
            "Warm, humid conditions",
            "Water splashing on leaves",
            "Poor air circulation"
        ],
        "treatment_steps": [
            "Remove and destroy infected leaves",
            "Apply copper-based bactericides",
            "Improve air circulation",
            "Avoid overhead watering",
            "Use disease-resistant varieties"
        ],
        "recommended_products": [
            "Copper Hydroxide spray",
            "Streptomycin sulfate",
            "Bacillus subtilis bio-fungicide"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Practice crop rotation",
            "Maintain proper plant spacing",
            "Water at soil level"
        ]
    },
    "Pepper__bell___healthy": {
        "disease_name": "Healthy Plant",
        "plant_type": "Bell Pepper",
        "severity": "None",
        "symptoms": [],
        "causes": [],
        "treatment_steps": [
            "Continue regular watering",
            "Maintain proper fertilization",
            "Monitor for early disease signs"
        ],
        "recommended_products": [
            "Balanced NPK fertilizer",
            "Organic compost"
        ],
        "prevention": [
            "Regular monitoring",
            "Proper nutrition",
            "Good cultural practices"
        ]
    },
    "Potato___Early_blight": {
        "disease_name": "Early Blight",
        "plant_type": "Potato",
        "severity": "Medium to High",
        "symptoms": [
            "Brown spots with concentric rings (target pattern)",
            "Yellowing around spots",
            "Lower leaves affected first",
            "Stem lesions"
        ],
        "causes": [
            "Alternaria solani fungus",
            "Warm temperatures (24-29°C)",
            "High humidity",
            "Plant stress"
        ],
        "treatment_steps": [
            "Remove infected leaves immediately",
            "Apply fungicide (Mancozeb or Chlorothalonil)",
            "Ensure proper spacing between plants",
            "Mulch to prevent soil splash",
            "Improve drainage"
        ],
        "recommended_products": [
            "Mancozeb 75% WP",
            "Chlorothalonil",
            "Azoxystrobin"
        ],
        "prevention": [
            "Use resistant varieties",
            "Crop rotation (3-4 years)",
            "Avoid overhead irrigation",
            "Remove plant debris"
        ]
    },
    "Potato___Late_blight": {
        "disease_name": "Late Blight",
        "plant_type": "Potato",
        "severity": "High (Very Serious)",
        "symptoms": [
            "Water-soaked lesions on leaves",
            "White fuzzy growth on leaf undersides",
            "Brown-black lesions on stems",
            "Tuber rot"
        ],
        "causes": [
            "Phytophthora infestans",
            "Cool, wet weather",
            "High humidity",
            "Poor air circulation"
        ],
        "treatment_steps": [
            "Apply systemic fungicides immediately",
            "Remove and destroy infected plants",
            "Improve ventilation",
            "Avoid irrigation during cool, humid periods",
            "Harvest early if disease is severe"
        ],
        "recommended_products": [
            "Metalaxyl + Mancozeb",
            "Cymoxanil + Mancozeb",
            "Dimethomorph"
        ],
        "prevention": [
            "Plant certified disease-free tubers",
            "Use resistant varieties",
            "Destroy volunteer plants",
            "Monitor weather conditions"
        ]
    },
    "Potato___healthy": {
        "disease_name": "Healthy Plant",
        "plant_type": "Potato",
        "severity": "None",
        "symptoms": [],
        "causes": [],
        "treatment_steps": [
            "Maintain regular care routine",
            "Continue proper watering and fertilization",
            "Monitor for disease signs"
        ],
        "recommended_products": [
            "Balanced NPK fertilizer",
            "Potassium-rich fertilizer for tuber development"
        ],
        "prevention": [
            "Regular monitoring",
            "Proper nutrition",
            "Good cultural practices"
        ]
    },
    "Tomato_Bacterial_spot": {
        "disease_name": "Bacterial Spot",
        "plant_type": "Tomato",
        "severity": "Medium to High",
        "symptoms": [
            "Small dark spots on leaves",
            "Spots with yellow halos",
            "Fruit lesions",
            "Leaf drop"
        ],
        "causes": [
            "Xanthomonas bacteria",
            "Warm, wet conditions",
            "Contaminated seeds or transplants"
        ],
        "treatment_steps": [
            "Remove infected plant parts",
            "Apply copper-based sprays",
            "Use bactericides",
            "Improve air circulation",
            "Reduce leaf wetness"
        ],
        "recommended_products": [
            "Copper hydroxide",
            "Copper oxychloride",
            "Streptomycin (where allowed)"
        ],
        "prevention": [
            "Use disease-free seeds",
            "Avoid overhead watering",
            "Practice crop rotation",
            "Disinfect tools"
        ]
    },
    "Tomato_Early_blight": {
        "disease_name": "Early Blight",
        "plant_type": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Dark brown spots with concentric rings",
            "Yellow tissue around spots",
            "Lower leaves affected first",
            "Fruit spots near stem"
        ],
        "causes": [
            "Alternaria solani fungus",
            "Warm humid weather",
            "Plant stress"
        ],
        "treatment_steps": [
            "Remove affected leaves",
            "Apply fungicides regularly",
            "Mulch around plants",
            "Stake plants for better air flow",
            "Water at base of plants"
        ],
        "recommended_products": [
            "Mancozeb",
            "Chlorothalonil",
            "Copper fungicides"
        ],
        "prevention": [
            "Crop rotation",
            "Use resistant varieties",
            "Proper spacing",
            "Remove plant debris"
        ]
    },
    "Tomato_Late_blight": {
        "disease_name": "Late Blight",
        "plant_type": "Tomato",
        "severity": "Very High (Critical)",
        "symptoms": [
            "Large brown water-soaked lesions",
            "White mold on leaf undersides",
            "Rapid plant collapse",
            "Brown firm fruit rot"
        ],
        "causes": [
            "Phytophthora infestans",
            "Cool wet weather",
            "High humidity"
        ],
        "treatment_steps": [
            "Apply systemic fungicides immediately",
            "Remove infected plants completely",
            "Destroy plant debris",
            "Avoid overhead watering",
            "Improve drainage"
        ],
        "recommended_products": [
            "Metalaxyl + Mancozeb",
            "Cymoxanil",
            "Dimethomorph + Mancozeb"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Ensure good air circulation",
            "Monitor weather forecasts",
            "Remove volunteer plants"
        ]
    },
    "Tomato_Leaf_Mold": {
        "disease_name": "Leaf Mold",
        "plant_type": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Yellow spots on upper leaf surface",
            "Olive-green to brown mold on undersides",
            "Leaf curling and death",
            "Reduced fruit quality"
        ],
        "causes": [
            "Passalora fulva fungus",
            "High humidity (>85%)",
            "Poor air circulation",
            "Greenhouse conditions"
        ],
        "treatment_steps": [
            "Reduce humidity below 85%",
            "Improve ventilation",
            "Remove infected leaves",
            "Apply fungicides",
            "Space plants properly"
        ],
        "recommended_products": [
            "Chlorothalonil",
            "Copper fungicides",
            "Biological fungicides (Bacillus)"
        ],
        "prevention": [
            "Use resistant varieties",
            "Maintain low humidity",
            "Proper plant spacing",
            "Greenhouse ventilation"
        ]
    },
    "Tomato_Septoria_leaf_spot": {
        "disease_name": "Septoria Leaf Spot",
        "plant_type": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Small circular spots with gray centers",
            "Dark borders around spots",
            "Tiny black dots in center (pycnidia)",
            "Lower leaves affected first"
        ],
        "causes": [
            "Septoria lycopersici fungus",
            "Warm wet weather",
            "Water splash on leaves"
        ],
        "treatment_steps": [
            "Remove infected lower leaves",
            "Apply fungicides preventively",
            "Mulch to prevent soil splash",
            "Water at plant base",
            "Stake plants"
        ],
        "recommended_products": [
            "Chlorothalonil",
            "Mancozeb",
            "Copper fungicides"
        ],
        "prevention": [
            "Crop rotation (3 years)",
            "Remove plant debris",
            "Avoid overhead watering",
            "Use disease-free transplants"
        ]
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "disease_name": "Two-Spotted Spider Mite",
        "plant_type": "Tomato",
        "severity": "Medium to High",
        "symptoms": [
            "Tiny yellow or white spots on leaves",
            "Fine webbing on leaves",
            "Bronzing of leaves",
            "Leaf drop in severe cases"
        ],
        "causes": [
            "Spider mite infestation",
            "Hot dry weather",
            "Dusty conditions",
            "Stressed plants"
        ],
        "treatment_steps": [
            "Spray plants with strong water stream",
            "Apply miticides or insecticidal soap",
            "Introduce predatory mites",
            "Increase humidity",
            "Remove heavily infested leaves"
        ],
        "recommended_products": [
            "Abamectin",
            "Spiromesifen",
            "Insecticidal soap",
            "Neem oil"
        ],
        "prevention": [
            "Regular monitoring",
            "Maintain plant health",
            "Avoid water stress",
            "Keep area dust-free"
        ]
    },
    "Tomato__Target_Spot": {
        "disease_name": "Target Spot",
        "plant_type": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Brown spots with concentric rings",
            "Target-like appearance",
            "Affects leaves, stems, and fruit",
            "Defoliation in severe cases"
        ],
        "causes": [
            "Corynespora cassiicola fungus",
            "Warm humid conditions",
            "Extended leaf wetness"
        ],
        "treatment_steps": [
            "Remove infected plant parts",
            "Apply fungicides",
            "Improve air circulation",
            "Reduce leaf wetness",
            "Mulch around plants"
        ],
        "recommended_products": [
            "Chlorothalonil",
            "Mancozeb",
            "Azoxystrobin"
        ],
        "prevention": [
            "Use resistant varieties",
            "Proper plant spacing",
            "Crop rotation",
            "Avoid overhead irrigation"
        ]
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "disease_name": "Tomato Yellow Leaf Curl Virus",
        "plant_type": "Tomato",
        "severity": "Very High (Critical)",
        "symptoms": [
            "Upward curling of leaves",
            "Yellowing of leaf margins",
            "Stunted plant growth",
            "Reduced fruit production",
            "Small, deformed fruits"
        ],
        "causes": [
            "Virus transmitted by whiteflies",
            "Warm climate",
            "High whitefly population"
        ],
        "treatment_steps": [
            "Remove and destroy infected plants",
            "Control whitefly population with insecticides",
            "Use yellow sticky traps",
            "Apply neem oil",
            "Use virus-resistant varieties"
        ],
        "recommended_products": [
            "Imidacloprid",
            "Thiamethoxam",
            "Acetamiprid",
            "Yellow sticky traps",
            "Reflective mulch"
        ],
        "prevention": [
            "Plant virus-resistant varieties",
            "Control whitefly from early stage",
            "Remove weeds (virus reservoirs)",
            "Use insect-proof nets",
            "Avoid planting near infected areas"
        ]
    },
    "Tomato__Tomato_mosaic_virus": {
        "disease_name": "Tomato Mosaic Virus",
        "plant_type": "Tomato",
        "severity": "High",
        "symptoms": [
            "Mottled light and dark green on leaves",
            "Leaf distortion",
            "Stunted growth",
            "Reduced fruit yield",
            "Fruit discoloration"
        ],
        "causes": [
            "Highly contagious virus",
            "Mechanical transmission",
            "Contaminated tools or hands",
            "Infected seeds"
        ],
        "treatment_steps": [
            "Remove and destroy infected plants",
            "Disinfect tools with 10% bleach solution",
            "Wash hands thoroughly",
            "Use virus-free seeds",
            "No chemical cure available"
        ],
        "recommended_products": [
            "10% bleach solution for tools",
            "Milk spray (may reduce spread)",
            "Virus-free certified seeds"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Sanitize tools regularly",
            "Avoid touching plants when wet",
            "Control weeds",
            "Don't use tobacco products near plants"
        ]
    },
    "Tomato_healthy": {
        "disease_name": "Healthy Plant",
        "plant_type": "Tomato",
        "severity": "None",
        "symptoms": [],
        "causes": [],
        "treatment_steps": [
            "Continue regular care",
            "Maintain consistent watering",
            "Provide adequate nutrition"
        ],
        "recommended_products": [
            "Balanced NPK fertilizer (10-10-10)",
            "Calcium supplement for fruit development",
            "Compost or organic matter"
        ],
        "prevention": [
            "Regular inspection",
            "Proper watering",
            "Good cultural practices",
            "Monitor for pests"
        ]
    }
}

# --------------- Generate Fertilizer Recommendation using Gemini ----------------
def get_fertilizer_recommendation(disease_label, plant_type):
    """Get fertilizer recommendation ONLY from Gemini API - No fallbacks"""
    
    if not gemini_available or not gemini_model:
        return {
            "success": False,
            "error": "AI recommendation service is currently unavailable. Please try again later."
        }
    
    try:
        if "healthy" in disease_label.lower():
            prompt = f"""For a healthy {plant_type} plant, recommend:
1. Best fertilizers for optimal growth (NPK ratios and specific products available in India)
2. Application schedule and dosage
3. Organic alternatives
4. Micronutrients needed

Provide specific product names available in Indian market."""
        else:
            prompt = f"""For {plant_type} affected by {disease_label}, recommend:
1. Fertilizers to boost plant immunity and recovery (specific NPK ratios and products)
2. Micronutrients that help fight this disease
3. Application timing and dosage
4. Organic options for treatment support
5. Fertilizers to avoid during disease treatment

Provide specific product names available in Indian agricultural market."""
        
        response = gemini_model.generate_content(prompt)
        
        return {
            "success": True,
            "recommendation": response.text,
            "disease": disease_label,
            "plant": plant_type
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Unable to generate recommendation: {str(e)}"
        }

# --------------- Generate Disease Information ----------------
def get_disease_information(disease_label):
    """Get structured disease information from database"""
    
    # Get structured information
    disease_data = DISEASE_INFO.get(disease_label, {})
    
    if not disease_data:
        # Fallback for unknown diseases
        disease_data = {
            "disease_name": disease_label.replace("_", " ").title(),
            "plant_type": "Unknown",
            "severity": "Unknown",
            "symptoms": ["Please consult an expert for accurate diagnosis"],
            "causes": ["Unknown"],
            "treatment_steps": ["Consult with local agricultural extension office"],
            "recommended_products": ["Consult agricultural store"],
            "prevention": ["Regular monitoring and good cultural practices"]
        }
    
    return disease_data

# --------------- Predict API ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "ML model not loaded"}), 500

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        image_bytes = file.read()

        img_arr = read_imagefile(image_bytes)

        # -------- LEAF VALIDATION --------
        if not is_leaf_image(img_arr):
            return jsonify({
                "error": "The uploaded image does not look like a leaf. Please upload a clear leaf image."
            }), 400

        # -------- PREDICTION --------
        with predict_lock:
            predictions = model.predict(img_arr)[0]

        index = int(np.argmax(predictions))
        disease_label = CLASS_NAMES[index]
        confidence = float(predictions[index])

        # Get disease information from database
        disease_info = get_disease_information(disease_label)
        plant_type = disease_info.get("plant_type", "Unknown")
        
        # Get fertilizer recommendation from Gemini API ONLY
        fertilizer_info = get_fertilizer_recommendation(disease_label, plant_type)

        # Prepare response
        response_data = {
            "success": True,
            "prediction": {
                "label": disease_label,
                "confidence": round(confidence * 100, 2),
                "confidence_percentage": f"{round(confidence * 100, 2)}%"
            },
            "disease_information": disease_info,
            "fertilizer_recommendation": fertilizer_info,
            "pesticide_stores": {
                "bing_maps_link": PESTICIDE_STORES_SEARCH_LINK,
                "description": "Click to find pesticide stores near you in Hyderabad"
            },
            "location": "Hyderabad, Telangana",
            "recommendations": {
                "immediate_action": disease_info.get("treatment_steps", [])[:3] if disease_info.get("treatment_steps") else [],
                "products_needed": disease_info.get("recommended_products", []),
                "severity_level": disease_info.get("severity", "Unknown")
            }
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        }), 500

# --------------- Health Check API ----------------
@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "database_ok": os.path.exists(DB_PATH),
        "gemini_available": gemini_available,
        "location": "Hyderabad, Telangana"
    })

# --------------- Run Server ----------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)