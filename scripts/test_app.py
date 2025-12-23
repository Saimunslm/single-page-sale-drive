#!/usr/bin/env python3
"""
Test script to verify the Flask application is working correctly.
This script tests various components of the application to ensure they function as expected.
"""

import os
import sys
from app import create_app
from models import ProductSetting, Review
from mongoengine.connection import disconnect


def test_app_creation():
    """Test that the Flask app can be created without errors."""
    print("Testing Flask app creation...")
    try:
        app = create_app('testing')
        print("✓ Flask app created successfully")
        return app
    except Exception as e:
        print(f"✗ Failed to create Flask app: {e}")
        return None


def test_database_connection(app):
    """Test that the database connection works."""
    print("\nTesting database connection...")
    try:
        with app.app_context():
            # Try to access the database
            settings = ProductSetting.objects.first()
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def test_theme_directories():
    """Test that all theme directories exist."""
    print("\nTesting theme directories...")
    themes_path = os.path.join(os.path.dirname(__file__), 'templates', 'themes')
    if not os.path.exists(themes_path):
        print("✗ Themes directory not found")
        return False
    
    themes = os.listdir(themes_path)
    required_templates = ['index.html', 'thank_you.html']
    
    for theme in themes:
        theme_path = os.path.join(themes_path, theme)
        if os.path.isdir(theme_path):
            print(f"  Checking theme: {theme}")
            for template in required_templates:
                template_path = os.path.join(theme_path, template)
                if not os.path.exists(template_path):
                    print(f"    ✗ Missing template: {template}")
                    return False
            print(f"    ✓ All templates present")
    
    print("✓ All theme directories are valid")
    return True


def test_static_files():
    """Test that static files directory exists and has required files."""
    print("\nTesting static files...")
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_path):
        print("✗ Static directory not found")
        return False
    
    images_path = os.path.join(static_path, 'images')
    if not os.path.exists(images_path):
        print("✗ Images directory not found")
        return False
    
    # Check for default product image
    default_image = os.path.join(images_path, 'honey_nut.png')
    if not os.path.exists(default_image):
        print("⚠ Default product image not found (honey_nut.png)")
    
    print("✓ Static files directory structure is valid")
    return True


def main():
    """Run all tests."""
    print("Running Flask Application Tests\n" + "="*40)
    
    # Test app creation
    app = test_app_creation()
    if not app:
        return 1
    
    # Test database connection
    if not test_database_connection(app):
        return 1
    
    # Test theme directories
    if not test_theme_directories():
        return 1
    
    # Test static files
    if not test_static_files():
        return 1
    
    print("\n" + "="*40)
    print("All tests passed! ✓")
    print("Your Flask application should work correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())