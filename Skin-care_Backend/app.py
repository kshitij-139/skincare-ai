"""
Main Flask Application - FIXED VERSION
Skincare Analysis API with Disease Detection, Skin Type Classification, and AI Chatbot
"""
from flask import Flask, jsonify
from flask_cors import CORS
import tensorflow as tf
import torch
import torch.nn as nn
from config import Config
from utils.chatbot import HybridChatbot

# Import route blueprints
from routes import disease_bp, skincare_bp, chatbot_bp
from routes.disease import init_disease_route
from routes.skincare import init_skincare_route
from routes.chatbot_route import init_chatbot_route

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# ============================================================
# LOAD AI MODELS AT STARTUP
# ============================================================

print("\n" + "=" * 70)
print("🚀 INITIALIZING SKINCARE ANALYSIS API")
print("=" * 70)

# ============================================================
# Configure GPU/CPU
# ============================================================

print("\n🖥️  Configuring devices...")

# TensorFlow GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ TensorFlow GPU Available: {len(gpus)} GPU(s)")
    except RuntimeError as e:
        print(f"⚠️  TensorFlow GPU configuration error: {e}")
else:
    print("⚠️  TensorFlow using CPU (slower)")

# PyTorch GPU
torch_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"✅ PyTorch Device: {torch_device}")

# ============================================================
# Load Disease Detection Models (SavedModel with TFSMLayer)
# ============================================================
import tensorflow as tf

print("\n📦 Loading Disease Detection Models (SavedModel with TFSMLayer)...")

disease_model1 = None
disease_model2 = None

try:
    print(f"   Loading DenseNet121 as TFSMLayer...")
    
    # Load as TFSMLayer (Keras 3 compatible)
    disease_model1 = tf.keras.layers.TFSMLayer(
        Config.DISEASE_MODEL1_PATH,
        call_endpoint='serving_default'
    )
    
    print(f"   ✅ DenseNet121 loaded: {Config.DISEASE_MODEL1_PATH}")
    
except Exception as e:
    print(f"   ❌ Failed to load DenseNet121: {e}")

try:
    print(f"   Loading EfficientNetB3 as TFSMLayer...")
    
    # Load as TFSMLayer (Keras 3 compatible)
    disease_model2 = tf.keras.layers.TFSMLayer(
        Config.DISEASE_MODEL2_PATH,
        call_endpoint='serving_default'
    )
    
    print(f"   ✅ EfficientNetB3 loaded: {Config.DISEASE_MODEL2_PATH}")
    
except Exception as e:
    print(f"   ❌ Failed to load EfficientNetB3: {e}")

if disease_model1 and disease_model2:
    print(f"✅ Disease Detection ENSEMBLE Ready!")
    print(f"   Classes: {len(Config.DISEASE_CLASSES)}")
else:
    print(f"⚠️  Warning: Disease ensemble incomplete")

# ============================================================
# Load Skin Type Model (PyTorch) - SMART AUTO-DETECT
# ============================================================

print("\n📦 Loading Skin Type Model (PyTorch - Auto-Detect)...")

skin_type_model = None

try:
    from torchvision import models
    
    # Load checkpoint first to inspect it
    checkpoint = torch.load(Config.SKIN_TYPE_MODEL_PATH, map_location=torch_device)
    
    # Check if it's a full model or state dict
    if isinstance(checkpoint, nn.Module):
        # It's a full model!
        print(f"   ✅ Checkpoint is a full model")
        skin_type_model = checkpoint
        skin_type_model.to(torch_device)
        skin_type_model.eval()
        print(f"✅ Skin Type Model loaded (full model)")
        
    else:
        # It's a state dict - need to reconstruct model
        print(f"   📦 Checkpoint is a state dict - reconstructing model...")
        
        # Extract state dict
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
            elif 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
            else:
                state_dict = checkpoint
        else:
            state_dict = checkpoint
        
        # Try to auto-detect architecture from keys
        first_key = list(state_dict.keys())[0]
        print(f"   First key: {first_key}")
        
        # Check if keys start with 'base_model' or 'features'
        if first_key.startswith('base_model.'):
            # Model has 'base_model' wrapper
            print(f"   Detected: Model with 'base_model' wrapper")
            
            class SkinTypeModel(nn.Module):
                def __init__(self, num_classes=3):
                    super(SkinTypeModel, self).__init__()
                    self.base_model = models.efficientnet_b0(weights=None)
                    num_features = self.base_model.classifier[1].in_features
                    self.base_model.classifier = nn.Sequential(
                        nn.Dropout(p=0.3, inplace=True),
                        nn.Linear(num_features, num_classes)
                    )
                
                def forward(self, x):
                    return self.base_model(x)
            
            skin_type_model = SkinTypeModel(num_classes=len(Config.SKIN_TYPE_CLASSES))
        
        elif first_key.startswith('features.'):
            # Direct EfficientNet model (no wrapper)
            print(f"   Detected: Direct EfficientNet model")
            skin_type_model = models.efficientnet_b0(weights=None)
            num_features = skin_type_model.classifier[1].in_features
            skin_type_model.classifier = nn.Sequential(
                nn.Dropout(p=0.3, inplace=True),
                nn.Linear(num_features, len(Config.SKIN_TYPE_CLASSES))
            )
        
        else:
            print(f"   ⚠️  Unknown architecture - trying generic load")
            # Try to load as-is
            skin_type_model = models.efficientnet_b0(weights=None)
        
        # Load state dict with strict=False
        print(f"   Loading state dict with strict=False...")
        incompatible_keys = skin_type_model.load_state_dict(
            state_dict,
            strict=False  # ✅ CRITICAL!
        )
        
        if incompatible_keys.missing_keys:
            print(f"   ⚠️  {len(incompatible_keys.missing_keys)} missing keys (OK with strict=False)")
            # Only show first 5
            for key in list(incompatible_keys.missing_keys)[:5]:
                print(f"      - {key}")
            if len(incompatible_keys.missing_keys) > 5:
                print(f"      ... and {len(incompatible_keys.missing_keys) - 5} more")
        
        if incompatible_keys.unexpected_keys:
            print(f"   ⚠️  {len(incompatible_keys.unexpected_keys)} unexpected keys (OK with strict=False)")
            for key in list(incompatible_keys.unexpected_keys)[:5]:
                print(f"      - {key}")
            if len(incompatible_keys.unexpected_keys) > 5:
                print(f"      ... and {len(incompatible_keys.unexpected_keys) - 5} more")
        
        # Move to device and eval
        skin_type_model.to(torch_device)
        skin_type_model.eval()
        
        print(f"✅ Skin Type Model loaded successfully!")
    
    print(f"   Device: {torch_device}")
    print(f"   Classes: {Config.SKIN_TYPE_CLASSES}")
    
    # Quick test prediction
    test_input = torch.randn(1, 3, 224, 224).to(torch_device)
    with torch.no_grad():
        test_output = skin_type_model(test_input)
    print(f"   Test output shape: {test_output.shape} ✅")

except Exception as e:
    print(f"❌ Failed to load skin type model")
    print(f"   Error: {str(e)}")
    print(f"   Type: {type(e).__name__}")
    skin_type_model = None

# ============================================================
# Load Chatbot - FIXED
# ============================================================

print("\n🤖 Loading FREE Hybrid Chatbot...")
try:
    chatbot = HybridChatbot(
        knowledge_file=Config.KNOWLEDGE_BASE_PATH,
        similarity_threshold=Config.SIMILARITY_THRESHOLD
    )
    print("✅ Chatbot ready!")
except Exception as e:
    print(f"❌ Failed to load chatbot: {e}")
    chatbot = None

# ============================================================
# Initialize Routes
# ============================================================

if disease_model1 and disease_model2:
    init_disease_route(disease_model1, disease_model2, Config.DISEASE_CLASSES)

if skin_type_model:
    init_skincare_route(
        skin_type_model,
        Config.SKIN_TYPE_CLASSES,
        torch_device,
        chatbot
    )

if chatbot:
    init_chatbot_route(chatbot)

# Register blueprints
app.register_blueprint(disease_bp, url_prefix='/api/disease')
app.register_blueprint(skincare_bp, url_prefix='/api/skincare')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

print("\n✅ All routes registered!")

# ============================================================
# ROOT ENDPOINTS
# ============================================================

@app.route('/')
def home():
    return jsonify({
        "message": "🧴 Skincare Analysis API",
        "version": "2.0 - Fixed",
        "models": {
            "disease_detection": {
                "status": "loaded" if (disease_model1 and disease_model2) else "failed",
                "format": "TFSMLayer (Keras 3 compatible)"
            },
            "skin_type": {
                "status": "loaded" if skin_type_model else "failed",
                "format": "PyTorch"
            },
            "chatbot": {
                "status": "loaded" if chatbot else "failed",
                "type": "HuggingFace + RapidFuzz"
            }
        },
        "endpoints": {
            "disease": "/api/disease/analyze",
            "skincare": "/api/skincare/analyze",
            "chatbot": "/api/chatbot/chat",
            "health": "/health"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "models": {
            "disease_densenet121": disease_model1 is not None,
            "disease_efficientnet": disease_model2 is not None,
            "skin_type": skin_type_model is not None,
            "chatbot": chatbot is not None
        },
        "gpu": {
            "tensorflow": len(tf.config.list_physical_devices('GPU')) > 0,
            "pytorch": torch.cuda.is_available()
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🎉 SKINCARE ANALYSIS API READY!")
    print("=" * 70)
    print(f"\n✅ Disease Detection:")
    print(f"   DenseNet121: {'Loaded' if disease_model1 else 'Failed'}")
    print(f"   EfficientNetB3: {'Loaded' if disease_model2 else 'Failed'}")
    print(f"✅ Skin Type: {'Loaded' if skin_type_model else 'Failed'}")
    print(f"✅ Chatbot: {'Loaded' if chatbot else 'Failed'}")
    print(f"\n📡 Server starting on http://0.0.0.0:5000")
    print("=" * 70 + "\n")
    
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=5000
    )