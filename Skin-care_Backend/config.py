"""
Configuration settings for the Flask app
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Disease Model paths (ENSEMBLE - SavedModel format)
    DISEASE_MODEL1_PATH = os.getenv('DISEASE_MODEL1_PATH', 'models/dermnet_densenet121_saved')
    DISEASE_MODEL2_PATH = os.getenv('DISEASE_MODEL2_PATH', 'models/dermnet_effnet_b3_saved')
    
    # Skin Type Model path (PyTorch)
    SKIN_TYPE_MODEL_PATH = os.getenv('SKIN_TYPE_MODEL_PATH', 'models/skin_type_model.pth')
    
    # Knowledge base
    KNOWLEDGE_BASE_PATH = 'data/skincare_knowledge.json'
    
    # Chatbot settings (FREE - No API keys needed!)
    SIMILARITY_THRESHOLD = int(os.getenv('SIMILARITY_THRESHOLD', '75'))
    USE_GPU_FOR_CHATBOT = os.getenv('USE_GPU_FOR_CHATBOT', 'False') == 'True'
    
    # Disease classes (23 classes from DermNet)
    DISEASE_CLASSES = [
        'Acne', 'Actinic Keratosis', 'Atopic Dermatitis', 'Basal Cell Carcinoma',
        'Benign Keratosis', 'Cellulitis', 'Chickenpox', 'Cutaneous Larva Migrans',
        'Eczema', 'Herpes', 'Impetigo', 'Melanoma', 'Monkeypox', 'Nail Fungus',
        'Poison Ivy', 'Psoriasis', 'Ringworm', 'Rosacea', 'Scabies',
        'Seborrheic Keratoses', 'Shingles', 'Tinea', 'Warts'
    ]
    
    # Skin type classes (PyTorch model)
    SKIN_TYPE_CLASSES = ['Dry', 'Normal', 'Oily']