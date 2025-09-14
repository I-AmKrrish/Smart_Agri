import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sensor_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # API settings
    API_PREFIX = '/api'
    
    # Model paths
    CROP_MODEL_PATH = 'models/crop_recommender_model.pkl'
    FERTILIZER_MODEL_PATH = 'models/fertilizer_recommender_model.pkl'