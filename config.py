import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'honey-nut-pro-secret-key-99'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Static file caching (30 days)
    SEND_FILE_MAX_AGE_DEFAULT = 2592000
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': os.environ.get('DEV_MONGODB_URI') or 'mongodb://localhost:27017/organic_shop_db'
    }

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_URI') or 'mongodb+srv://new_royal_bd:SNyA6P0eaALBp6th@newroyalbd.b9dwiuy.mongodb.net/organic_shop_db?appName=newroyalbd'
    }

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGODB_SETTINGS = {
        'host': 'mongomock://localhost'
    }

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}