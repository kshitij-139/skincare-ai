import React, { useState } from 'react';
import { Upload, Loader, AlertCircle, CheckCircle } from 'lucide-react';
import { detectDisease } from '../services/api';
import DiseaseResults from './Results/DiseaseResults';

const DiseaseDetection = () => {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
      setResults(null);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!image) {
      setError('Please upload an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await detectDisease(image);
      setResults(data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>🔬 Disease Detection</h1>
        <p>Upload an image to detect skin diseases</p>
      </div>

      <div className="upload-section">
        <div className="upload-card">
          {!imagePreview ? (
            <label className="upload-area">
              <Upload size={48} />
              <h3>Upload Skin Image</h3>
              <p>Click to browse or drag and drop</p>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                style={{ display: 'none' }}
              />
            </label>
          ) : (
            <div className="image-preview-container">
              <img src={imagePreview} alt="Preview" className="image-preview" />
              <button 
                className="btn-secondary"
                onClick={() => {
                  setImage(null);
                  setImagePreview(null);
                  setResults(null);
                }}
              >
                Change Image
              </button>
            </div>
          )}
        </div>

        {imagePreview && !results && (
          <button 
            className="btn-primary"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader className="spinner" size={20} />
                Analyzing...
              </>
            ) : (
              'Analyze Image'
            )}
          </button>
        )}

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={20} />
            {error}
          </div>
        )}
      </div>

      {results && <DiseaseResults results={results} />}
    </div>
  );
};

export default DiseaseDetection;