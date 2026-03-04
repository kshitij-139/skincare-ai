import React from 'react';
import { CheckCircle, AlertTriangle, TrendingUp } from 'lucide-react';

const DiseaseResults = ({ results }) => {
  const { disease_detected, top_prediction, all_predictions, recommendation } = results;

  return (
    <div className="results-container">
      <div className={`results-header ${disease_detected ? 'warning' : 'success'}`}>
        {disease_detected ? (
          <>
            <AlertTriangle size={32} />
            <h2>Disease Detected</h2>
          </>
        ) : (
          <>
            <CheckCircle size={32} />
            <h2>No Major Diseases Detected</h2>
          </>
        )}
      </div>

      <div className="results-content">
        <div className="top-prediction">
          <h3>Top Prediction</h3>
          <div className="prediction-card primary">
            <div className="prediction-info">
              <h4>{top_prediction.disease}</h4>
              <div className="confidence-bar">
                <div 
                  className="confidence-fill"
                  style={{ width: `${top_prediction.confidence}%` }}
                />
              </div>
              <span className="confidence-text">
                {top_prediction.confidence.toFixed(2)}% confidence
              </span>
            </div>
          </div>
        </div>

        <div className="all-predictions">
          <h3>
            <TrendingUp size={20} />
            All Predictions
          </h3>
          {all_predictions.map((pred, index) => (
            <div key={index} className="prediction-card">
              <div className="prediction-rank">#{index + 1}</div>
              <div className="prediction-info">
                <h4>{pred.disease}</h4>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${pred.confidence}%` }}
                  />
                </div>
                <span className="confidence-text">
                  {pred.confidence.toFixed(2)}%
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className={`recommendation ${disease_detected ? 'warning' : 'success'}`}>
          <h3>Recommendation</h3>
          <p>{recommendation}</p>
        </div>
      </div>
    </div>
  );
};

export default DiseaseResults;