"""
Image preprocessing utilities for both TensorFlow and PyTorch
"""
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import io

def preprocess_image_tensorflow(image_data, target_size=(224, 224)):
    """
    Preprocess image for TensorFlow models (Disease Detection)
    
    Args:
        image_data: Binary image data
        target_size: Target image size (width, height)
    
    Returns:
        Preprocessed numpy array for TensorFlow
    """
    try:
        # Open image
        img = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Resize
        img = img.resize(target_size)
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        raise ValueError(f"Error preprocessing image for TensorFlow: {str(e)}")

def preprocess_image_pytorch(image_data, target_size=(224, 224)):
    """
    Preprocess image for PyTorch models (Skin Type)
    
    Args:
        image_data: Binary image data
        target_size: Target image size (width, height)
    
    Returns:
        Preprocessed PyTorch tensor
    """
    try:
        # Open image
        img = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Define transforms (same as training)
        transform = transforms.Compose([
            transforms.Resize(target_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Apply transforms
        img_tensor = transform(img)
        
        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0)
        
        return img_tensor
    
    except Exception as e:
        raise ValueError(f"Error preprocessing image for PyTorch: {str(e)}")

# Keep backward compatibility
def preprocess_image(image_data, target_size=(224, 224)):
    """Default preprocessing (TensorFlow)"""
    return preprocess_image_tensorflow(image_data, target_size)