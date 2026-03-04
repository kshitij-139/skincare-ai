"""
Disease Detection Routes - TFSMLayer Compatible
"""
from flask import Blueprint, request, jsonify
from utils.image_processing import preprocess_image_tensorflow
import numpy as np
import tensorflow as tf

disease_bp = Blueprint('disease', __name__)

disease_model1 = None
disease_model2 = None
DISEASE_CLASSES = []

def init_disease_route(model1, model2, classes):
    global disease_model1, disease_model2, DISEASE_CLASSES
    disease_model1 = model1
    disease_model2 = model2
    DISEASE_CLASSES = classes

@disease_bp.route('/analyze', methods=['POST'])
def analyze_disease():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image"}), 400
        
        image_data = request.files['image'].read()
        img_array = preprocess_image_tensorflow(image_data)
        
        # Convert to tensor
        img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
        
        # Predict with TFSMLayer (returns dict)
        pred1_dict = disease_model1(img_tensor)
        pred2_dict = disease_model2(img_tensor)
        
        # Extract output (key might vary, usually 'output_0' or similar)
        # Check what keys are available
        pred1_key = list(pred1_dict.keys())[0]
        pred2_key = list(pred2_dict.keys())[0]
        
        predictions1 = pred1_dict[pred1_key].numpy()
        predictions2 = pred2_dict[pred2_key].numpy()
        
        # Ensemble
        ensemble_pred = (predictions1 + predictions2) / 2.0
        
        # Get top 3
        top_indices = np.argsort(ensemble_pred[0])[-3:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "disease": DISEASE_CLASSES[idx],
                "confidence": float(ensemble_pred[0][idx] * 100)
            })
        
        top_disease = results[0]
        disease_detected = top_disease['confidence'] > 50
        
        return jsonify({
            "success": True,
            "disease_detected": disease_detected,
            "top_prediction": top_disease,
            "all_predictions": results,
            "recommendation": "⚕️ Consult dermatologist" if disease_detected else "✅ No major diseases detected"
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500