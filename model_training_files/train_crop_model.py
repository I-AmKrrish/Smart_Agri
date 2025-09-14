import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load and prepare dataset (example)
def load_crop_data():
    # In real implementation, load from database or CSV
    # This is sample data for demonstration
    data = {
        'moisture': np.random.uniform(10, 80, 1000),
        'temperature': np.random.uniform(10, 40, 1000),
        'humidity': np.random.uniform(20, 90, 1000),
        'nitrogen': np.random.randint(10, 200, 1000),
        'phosphorus': np.random.randint(5, 150, 1000),
        'potassium': np.random.randint(20, 300, 1000),
        'crop': np.random.choice([
            'Wheat', 'Rice', 'Maize', 'Barley', 'Pearl Millet', 
            'Chickpea', 'Kidney Beans', 'Pigeon Peas', 'Moth Beans',
            'Cotton', 'Sugarcane', 'Tobacco', 'Groundnut'
        ], 1000)
    }
    
    return pd.DataFrame(data)

def train_crop_model():
    # Load data
    df = load_crop_data()
    
    # Prepare features and target
    X = df.drop('crop', axis=1)
    y = df['crop']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = CatBoostClassifier(verbose=0)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save model
    joblib.dump(model, 'crop_recommender_model.pkl')
    print("Model saved as crop_recommender_model.pkl")
    
    return model

if __name__ == "__main__":
    train_crop_model()