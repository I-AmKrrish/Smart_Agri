from catboost import CatBoostClassifier
import numpy as np
import pandas as pd
import joblib

class CropRecommender:
    def __init__(self, model_path=None):
        if model_path:
            self.model = joblib.load(model_path)
        else:
            self.model = CatBoostClassifier(verbose=0)
        
        # Crop labels (example)
        self.crop_labels = [
            'Wheat', 'Rice', 'Maize', 'Barley', 'Pearl Millet', 
            'Chickpea', 'Kidney Beans', 'Pigeon Peas', 'Moth Beans',
            'Cotton', 'Sugarcane', 'Tobacco', 'Groundnut'
        ]
    
    def train(self, X, y):
        self.model.fit(X, y)
        joblib.dump(self.model, 'crop_recommender_model.pkl')
    
    def recommend_crop(self, features):
        prediction = self.model.predict(features)
        probabilities = self.model.predict_proba(features)
        
        # Get top 3 recommendations
        top_3_idx = np.argsort(probabilities[0])[-3:][::-1]
        recommendations = [
            {
                'crop': self.crop_labels[idx],
                'probability': round(float(probabilities[0][idx]), 3)
            }
            for idx in top_3_idx
        ]
        
        return recommendations