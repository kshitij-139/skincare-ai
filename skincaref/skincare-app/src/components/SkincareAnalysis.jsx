import React, { useState } from 'react';
import { Upload, Loader, AlertCircle, Sparkles } from 'lucide-react';
import { analyzeSkincareWithQuestionnaire } from '../services/api';
import Questionnaire from './Questionnaire';
import SkincareResults from './Results/SkincareResults';

const SkincareAnalysis = () => {
  const [step, setStep] = useState(1); // 1: Upload, 2: Questionnaire, 3: Results
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [questionnaire, setQuestionnaire] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleNextToQuestionnaire = () => {
    if (!image) {
      setError('Please upload an image first');
      return;
    }
    setStep(2);
  };

  const handleQuestionnaireSubmit = async (questionnaireData) => {
    setQuestionnaire(questionnaireData);
    setLoading(true);
    setError(null);

    try {
      const data = await analyzeSkincareWithQuestionnaire(image, questionnaireData);
      setResults(data);
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze. Please try again.');
      setStep(2);
    } finally {
      setLoading(false);
    }
  };

  const handleStartOver = () => {
    setStep(1);
    setImage(null);
    setImagePreview(null);
    setQuestionnaire(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>✨ Skincare Analysis</h1>
        <p>Get your personalized skincare routine with natural & commercial options</p>
      </div>

      {/* Step 1: Upload Image */}
      {step === 1 && (
        <div className="upload-section">
          <div className="upload-card">
            {!imagePreview ? (
              <label className="upload-area">
                <Upload size={48} />
                <h3>Upload Your Photo</h3>
                <p>Take a clear photo of your face in good lighting</p>
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
                  }}
                >
                  Change Image
                </button>
              </div>
            )}
          </div>

          {imagePreview && (
            <button 
              className="btn-primary"
              onClick={handleNextToQuestionnaire}
            >
              Next: Answer Questions
              <Sparkles size={20} />
            </button>
          )}

          {error && (
            <div className="alert alert-error">
              <AlertCircle size={20} />
              {error}
            </div>
          )}
        </div>
      )}

      {/* Step 2: Questionnaire */}
      {step === 2 && (
        <Questionnaire 
          onSubmit={handleQuestionnaireSubmit}
          onBack={() => setStep(1)}
          loading={loading}
        />
      )}

      {/* Step 3: Results */}
      {step === 3 && results && (
        <SkincareResults 
          results={results}
          onStartOver={handleStartOver}
        />
      )}
    </div>
  );
};

export default SkincareAnalysis;