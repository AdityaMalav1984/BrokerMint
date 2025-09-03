# backend/config.py - UPDATED
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base
    SECRET_KEY = os.getenv('SECRET_KEY', 'brokermint-dev-secret-2024')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    # Database
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'shared_data', 'brokermint.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Paths
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'shared_data')
    UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
    
    # Anomaly Detection
    ANOMALY_THRESHOLDS = {
        'Low': 0.3,
        'Medium': 0.6,
        'High': 0.8,
        'Critical': 0.95
    }

config = Config()