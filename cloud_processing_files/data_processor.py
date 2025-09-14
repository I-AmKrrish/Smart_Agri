from datetime import datetime
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.sensor_data = pd.DataFrame(columns=[
            'timestamp', 'moisture', 'temperature', 'humidity', 
            'nitrogen', 'phosphorus', 'potassium', 'device_id'
        ])
    
    def process_incoming_data(self, data):
        # Add timestamp to data
        data['timestamp'] = datetime.now().isoformat()
        
        # Convert to DataFrame and append
        new_row = pd.DataFrame([data])
        self.sensor_data = pd.concat([self.sensor_data, new_row], ignore_index=True)
        
        # Save to database (in real implementation)
        self.save_to_database(data)
        
        return data
    
    def save_to_database(self, data):
        # In real implementation, save to database
        pass
    
    def prepare_features(self):
        # Prepare features for ML models
        features = self.sensor_data[[
            'moisture', 'temperature', 'humidity', 
            'nitrogen', 'phosphorus', 'potassium'
        ]].copy()
        
        # Add derived features
        features['n_p_ratio'] = features['nitrogen'] / features['phosphorus']
        features['n_k_ratio'] = features['nitrogen'] / features['potassium']
        features['p_k_ratio'] = features['phosphorus'] / features['potassium']
        
        # Handle missing values
        features.fillna(features.mean(), inplace=True)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        return scaled_features, features.columns.tolist()