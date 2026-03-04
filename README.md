# 🧴 SkinCare AI

AI-powered skin analysis platform with disease detection, personalized skincare routines, and AI chatbot assistance.

## ✨ Features

- 🔬 **Disease Detection** - 93% accurate detection of 23 skin diseases
- 💆 **Skincare Analysis** - Personalized routines based on skin type (Dry/Normal/Oily)
- 💬 **AI Chatbot** - 24/7 skincare advice with natural remedies
- 🌿 **Natural + Commercial Options** - Home remedies alongside product recommendations

## 🚀 Quick Setup

### Prerequisites

- **Python 3.12** - https://www.python.org/downloads/
- **Node.js 18+** - https://nodejs.org/

### Installation
```bash
# 1. Clone repository
git clone https://github.com/yourusername/skincare-ai.git
cd skincare-ai

# 2. Setup Backend
cd skincare-backend
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows
pip install -r requirements.txt

# 3. Setup Frontend
cd ../skincaref/skincare-app
npm install

# 4. Add Model Files
# Download models from: [YOUR GOOGLE DRIVE LINK]
# Extract to: skincare-backend/models/
```

### Running

**Terminal 1 (Backend):**
```bash
cd skincare-backend
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd skincaref/skincare-app
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend: http://localhost:5000

## 📂 Project Structure
```
skincare-ai/
├── skincare-backend/       # Flask API
│   ├── models/            # AI models (download separately)
│   ├── routes/            # API endpoints
│   ├── utils/             # Helper functions
│   └── app.py
└── skincaref/
    └── skincare-app/      # React UI
```

## 📊 Tech Stack

**Backend:**
- Flask
- TensorFlow 2.15 (Disease Detection Ensemble)
- PyTorch 2.1 (Skin Type Classification)
- HuggingFace Transformers (Chatbot)

**Frontend:**
- React 18 + Vite
- Modern CSS (No frameworks)
- Axios

## 🤝 Contributing

Pull requests are welcome!

## 📝 License

MIT

---

Made with 💙