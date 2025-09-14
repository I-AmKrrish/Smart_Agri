import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import joblib

# Load and prepare dataset (example)
def load_fertilizer_data():
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
            'Wheat', 'Rice', 'Maize', 'Cotton', 'Sugarcane'
        ], 1000),
        'fertilizer': np.random.choice([
            'Urea', 'DAP', 'MOP', 'SSP', 'NPK 10-26-26',
            'NPK 12-32-16', 'Ammonium Sulfate', 'Calcium Nitrate'
        ], 1000)
    }
    
    return pd.DataFrame(data)

def train_fertilizer_model():
    # Load data
    df = load_fertilizer_data()
    
    # Prepare features and target
    X = df.drop(['fertilizer', 'crop'], axis=1)
    y = df['fertilizer']
    
    # Add crop as a feature (one-hot encoding)
    X = pd.concat([X, pd.get_dummies(df['crop'])], axis=1)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Define parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    }
    
    # Train model with GridSearchCV
    model = GridSearchCV(
        RandomForestClassifier(), 
        param_grid, 
        cv=5, 
        scoring='accuracy'
    )
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    print(f"Best parameters: {model.best_params_}")
    
    # Save model
    joblib.dump(model, 'fertilizer_recommender_model.pkl')
    print("Model saved as fertilizer_recommender_model.pkl")
    
    return model

if __name__ == "__main__":
    train_fertilizer_model()