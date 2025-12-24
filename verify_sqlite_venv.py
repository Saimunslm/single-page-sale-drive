from app import create_app, db
from models import Admin, ProductSetting
import os
import sys

print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

try:
    import flask_sqlalchemy
    print(f"Flask-SQLAlchemy version: {flask_sqlalchemy.__version__}")
except ImportError:
    print("CRITICAL: Flask-SQLAlchemy NOT found!")
    sys.exit(1)

app = create_app('production')

with app.app_context():
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site.db')
    print(f"Database path: {db_path}")
    
    print("Creating database tables...")
    db.create_all()
    print("Tables created.")
    
    admin = Admin.query.first()
    if admin:
        print(f"Admin found: {admin.username}")
    else:
        print("Admin not found (should have been created by create_app)")
        
    settings = ProductSetting.query.first()
    if settings:
        print(f"Settings found: {settings.shop_name}")
    else:
        print("Settings not found")
        
    print("Migration Verification Successful.")
