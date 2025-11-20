# 🌿 Plant Disease Detection Using EfficientNet-B3 & Flask

A deep-learning powered web application that detects plant leaf diseases using the **EfficientNet-B3** model trained on the **PlantVillage dataset**.  
Users can upload an image of a leaf, and the system predicts the disease with confidence and provides treatment recommendations.

---

## 🚀 Features

- 🌱 **AI-based leaf disease prediction**
- 📷 Upload leaf images through a clean web interface
- 🧠 Model architecture: **EfficientNet-B3**
- 💬 Treatment recommendations for each predicted disease
- 🔐 Secure user authentication (SQLite database)
- ⚡ Fast real-time prediction using Flask backend
- 🎨 Responsive UI using HTML + CSS

---

## 📁 Project Structure

PLANT-DISEASE-DETECTION/
│
├── app.py
├── app2.py
├── requirements.txt
├── users.db
├── .gitignore
│
├── model/ # Trained EfficientNet-B3 model
├── dataset/ # Original training dataset (ignored in repo)
│
├── static/
│ └── css, js, images
│
└── templates/
└── index.html, result.html, login.html

yaml
Copy code

---

## 🧪 Technologies Used

- **Python 3**
- **Flask**
- **TensorFlow / Keras**
- **EfficientNet-B3**
- **HTML, CSS, JavaScript**
- **SQLite**

---

## 🔥 How It Works

1. User uploads a leaf image  
2. The system preprocesses it (resize: 224×224)  
3. EfficientNet-B3 model predicts the disease  
4. Output includes:
   - Disease name  
   - Confidence percentage  
   - Treatment suggestions  

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

shell
Copy code

### 2️⃣ Create & activate virtual environment

python -m venv venv
venv\Scripts\activate # Windows

shell
Copy code

### 3️⃣ Install required libraries

pip install -r requirements.txt

shell
Copy code

### 4️⃣ Run the Flask server

python app.py

yaml
Copy code

Open your browser and visit:

👉 **http://127.0.0.1:5000**

---


## 📌 Future Enhancements

- Mobile app version    
- Advanced multi-disease detection  
- Deployment on AWS / Render / Railway  

---


