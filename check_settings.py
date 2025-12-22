from app import create_app
from models import db, ProductSetting, Admin
import os

app = create_app()
with app.app_context():
    settings_count = ProductSetting.query.count()
    print(f"Total ProductSetting rows: {settings_count}")
    
    settings = ProductSetting.query.all()
    for s in settings:
        print(f"ID: {s.id}, Shop: {s.shop_name}, Image: {s.image_path}, Landing Theme: {s.landing_page_theme}")
    
    admins = Admin.query.all()
    print(f"Admins: {[a.username for a in admins]}")
    
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'orders.db')
    print(f"Database Absolute Path: {db_path}")
    print(f"Database exists at absolute path: {os.path.exists(db_path)}")
    
    print(f"Current Working Directory: {os.getcwd()}")

