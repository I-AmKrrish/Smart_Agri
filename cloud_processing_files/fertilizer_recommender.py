from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
import joblib

class FertilizerRecommender:
    def __init__(self, model_path=None):
        if model_path:
            self.model = joblib.load(model_path)
        else:
            # Define parameter grid for GridSearchCV
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5, 10]
            }
            self.model = GridSearchCV(
                RandomForestClassifier(), 
                param_grid, 
                cv=5, 
                scoring='accuracy'
            )
        
        # Fertilizer labels (example)
        self.fertilizer_labels = [
            'Urea', 'DAP', 'MOP', 'SSP', 'NPK 10-26-26',
            'NPK 12-32-16', 'Ammonium Sulfate', 'Calcium Nitrate'
        ]
    
    def train(self, X, y):
        self.model.fit(X, y)
        joblib.dump(self.model, 'fertilizer_recommender_model.pkl')
    
    def recommend_fertilizer(self, features, current_crop):
        prediction = self.model.predict(features)
        probabilities = self.model.predict_proba(features)
        
        # Get top recommendation
        top_idx = np.argmax(probabilities[0])
        recommendation = {
            'fertilizer': self.fertilizer_labels[top_idx],
            'probability': round(float(probabilities[0][top_idx]), 3),
            'crop': current_crop
        }
        
        return recommendation