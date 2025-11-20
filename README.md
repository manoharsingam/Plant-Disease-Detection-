# 🌾 Agricure - Plant Disease Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Agricure** is an AI-powered plant disease detection web application that helps farmers and gardeners identify diseases in tomato, potato, and bell pepper plants. The system provides instant diagnosis, treatment recommendations, and connects users with local agricultural product suppliers.

## 🌟 Features

### Core Functionality
- 🔬 **AI-Powered Disease Detection** - Deep learning model trained on 15 plant disease classes
- 📸 **Image Upload & Camera Capture** - Flexible image input options
- 🍃 **Leaf Validation** - Automatic verification to ensure uploaded images are plant leaves
- 💊 **Treatment Recommendations** - Detailed treatment steps for identified diseases
- 🌱 **Fertilizer Guidance** - AI-generated fertilizer recommendations using Google Gemini API
- 🏪 **Product Store** - Browse and purchase agricultural products (fungicides, insecticides, fertilizers)
- 📍 **Local Store Finder** - Bing Maps integration for finding pesticide stores in Hyderabad

### User Experience
- 🔐 **User Authentication** - Secure signup and login system
- 🎨 **Modern UI** - Beautiful agricultural-themed interface with smooth animations
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- ⚡ **Real-time Analysis** - Fast disease detection with confidence scores

## 📋 Supported Plants & Diseases

### Bell Pepper (2 classes)
- Bacterial Spot
- Healthy

### Potato (3 classes)
- Early Blight
- Late Blight
- Healthy

### Tomato (10 classes)
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites (Two-Spotted)
- Target Spot
- Yellow Leaf Curl Virus
- Mosaic Virus
- Healthy

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep learning model (EfficientNet)
- **OpenCV** - Image processing and leaf validation
- **SQLite** - User authentication database
- **Google Gemini API** - AI-powered fertilizer recommendations

### Frontend
- **HTML5/CSS3** - Modern, responsive design
- **JavaScript (Vanilla)** - Interactive UI without frameworks
- **Flask Jinja2** - Template engine

### AI Model
- **Architecture**: EfficientNet-based CNN
- **Input Size**: 300x300 pixels
- **Training Dataset**: PlantVillage dataset
- **Accuracy**: High accuracy on validation set

## 📁 Project Structure

```
agricure/
├── model/
│   └── perfect_fit_final.h5          # Trained disease detection model
├── static/
│   ├── images/                        # Product images
│   │   ├── copper-hydroxide-spray.jpg
│   │   ├── mancozeb.jpg
│   │   ├── neem-oil.jpg
│   │   └── ... (25 product images)
│   └── main.js                        # Frontend JavaScript
├── templates/
│   ├── index.html                     # Login page
│   ├── signup.html                    # Signup page
│   ├── home.html                      # Main dashboard
│   └── store.html                     # Product store
├── app.py                             # Flask application (main backend)
├── users.db                           # SQLite database (auto-generated)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (for fertilizer recommendations)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/agricure.git
cd agricure
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
Edit `app.py` and add your Google Gemini API key:
```python
GEMINI_API_KEY = "your-gemini-api-key-here"
```

### Step 5: Add Product Images
Place your product images in the `static/images/` folder with these exact filenames:
- `copper-hydroxide-spray.jpg`
- `mancozeb.jpg`
- `neem-oil.jpg`
- ... (see complete list in app.py)

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📦 Requirements

Create a `requirements.txt` file with:

```txt
Flask==2.3.0
tensorflow==2.13.0
opencv-python==4.8.0
Pillow==10.0.0
numpy==1.24.3
google-generativeai==0.3.0
werkzeug==2.3.0
```

## 🎯 Usage

### 1. Create an Account
- Navigate to `http://localhost:5000`
- Click "Create one now" to sign up
- Fill in username, email, and password

### 2. Detect Plant Disease
- Login with your credentials
- Click "Upload Image" or "Capture Photo"
- Select/capture a clear image of a plant leaf
- Click "Analyze Plant"

### 3. View Results
- Disease name and confidence score
- Severity level
- Symptoms and causes
- Treatment steps
- Recommended products
- AI-generated fertilizer recommendations

### 4. Browse Product Store
- Click "Supplement Store" on the home page
- Filter by category (Fungicides, Insecticides, Fertilizers)
- Search for specific products
- Click "Buy on Amazon" to purchase
- Use "Local Stores" to find shops in Hyderabad

## 🔑 Key Features Explained

### Leaf Validation
The system uses HSV color space analysis to verify that uploaded images contain plant leaves (at least 25% green pixels required).

### Disease Detection
- Uses pre-trained EfficientNet model
- Preprocesses images to 300x300 pixels
- Returns disease class with confidence score

### Fertilizer Recommendations
- Powered by Google Gemini AI
- Provides specific NPK ratios
- Includes application schedules
- Suggests products available in Indian market

### Product Store
- 26 agricultural products across 3 categories
- Direct Amazon India purchase links
- Bing Maps integration for local stores in Hyderabad

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Login page |
| `/signup` | GET | Signup page |
| `/home` | GET | Main dashboard |
| `/store` | GET | Product store |
| `/api/signup` | POST | Create new user account |
| `/api/login` | POST | User authentication |
| `/predict` | POST | Disease detection (requires image file) |
| `/api/health` | GET | System health check |

## 🔒 Security Features

- Password hashing using Werkzeug security
- SQL injection prevention with parameterized queries
- Session-based authentication
- Input validation for image uploads

## 🎨 Design Philosophy

Agricure features a modern, agricultural-themed design with:
- Fresh green color palette (#2ecc71, #27ae60)
- Smooth animations and transitions
- Floating leaf background elements
- Mobile-first responsive design
- Intuitive user interface

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 🙏 Acknowledgments

- PlantVillage dataset for training data
- TensorFlow and Keras teams
- Google Gemini API for AI recommendations
- Flask community
- All contributors and testers



## 🔮 Future Enhancements

- [ ] Support for more plant species
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Disease progression tracking
- [ ] Community forum
- [ ] Weather integration
- [ ] Crop calendar
- [ ] Expert consultation feature

## 📊 Model Performance

- **Training Accuracy**: 95%+
- **Validation Accuracy**: 92%+
- **Inference Time**: < 1 second per image
- **Supported Image Formats**: JPG, PNG, JPEG


---

Made with 💚 for farmers and agriculture enthusiasts worldwide

**⭐ Star this repo if you find it helpful!**
