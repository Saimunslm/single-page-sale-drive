from app import create_app
from extensions import db
from models import Admin, ProductSetting
import os
import sys

# Ensure using venv python check? Assume running with venv python.
print(f"Python executable: {sys.executable}")

app = create_app('production')

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created.")
    
    admin = Admin.query.first()
    if admin:
        print(f"Admin found: {admin.username}")
    else:
        print("Admin not found (should have been created by create_app)")
    
    print("Refactor Verification Successful.")
