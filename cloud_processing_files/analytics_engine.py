import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class AnalyticsEngine:
    def __init__(self, historical_data):
        self.historical_data = historical_data
    
    def predict_yield(self, current_conditions, crop_type):
        # Simple linear model for demonstration
        # In real implementation, use more sophisticated models
        base_yield = {
            'Wheat': 3000,  # kg/ha
            'Rice': 4000,
            'Maize': 5000,
            'Cotton': 800
        }
        
        # Adjust yield based on conditions
        moisture_factor = min(1.0, current_conditions['moisture'] / 60)
        nutrient_factor = np.mean([
            min(1.0, current_conditions['nitrogen'] / 100),
            min(1.0, current_conditions['phosphorus'] / 50),
            min(1.0, current_conditions['potassium'] / 150)
        ])
        
        predicted_yield = base_yield.get(crop_type, 3000) * moisture_factor * nutrient_factor
        
        return round(predicted_yield, 2)
    
    def detect_water_stress(self, moisture_data):
        # Check if moisture is below threshold for consecutive readings
        stress_threshold = 30  # percent
        consecutive_dry_days = 0
        
        for moisture in moisture_data[-5:]:  # Check last 5 readings
            if moisture < stress_threshold:
                consecutive_dry_days += 1
            else:
                consecutive_dry_days = 0
        
        return consecutive_dry_days >= 3
    
    def assess_crop_health(self, conditions):
        # Calculate a health score based on multiple factors
        moisture_score = min(1.0, conditions['moisture'] / 60)
        temp_score = 1.0 - abs(conditions['temperature'] - 25) / 30  # Optimal around 25°C
        nutrient_score = np.mean([
            min(1.0, conditions['nitrogen'] / 100),
            min(1.0, conditions['phosphorus'] / 50),
            min(1.0, conditions['potassium'] / 150)
        ])
        
        health_score = (moisture_score * 0.4 + temp_score * 0.3 + nutrient_score * 0.3) * 100
        
        return round(health_score, 2)
    
    def generate_alerts(self, current_data, historical_data):
        alerts = []
        
        # Water stress alert
        if self.detect_water_stress(historical_data['moisture']):
            alerts.append({
                'type': 'water_stress',
                'message': 'Water stress detected - irrigation recommended',
                'severity': 'high'
            })
        
        # Nutrient deficiency alerts
        if current_data['nitrogen'] < 30:
            alerts.append({
                'type': 'nutrient_deficiency',
                'message': 'Nitrogen level low',
                'severity': 'medium'
            })
        
        if current_data['phosphorus'] < 15:
            alerts.append({
                'type': 'nutrient_deficiency',
                'message': 'Phosphorus level low',
                'severity': 'medium'
            })
        
        if current_data['potassium'] < 50:
            alerts.append({
                'type': 'nutrient_deficiency',
                'message': 'Potassium level low',
                'severity': 'medium'
            })
        
        return alerts