import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from flask_login import LoginManager
from config import config
from extensions import db

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'production')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.admin_login'
    
    # Import models
    from models import Admin, ProductSetting
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Admin.query.get(int(user_id))
        except:
            return None
    
    # Register blueprints
    from routes.main import main_bp
    from routes.orders import orders_bp
    from routes.admin import admin_bp
    from routes.health import health_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(health_bp)
    
    # Custom Jinja filters
    @app.template_filter('bn_digits')
    def bn_digits_filter(s):
        s = str(s)
        eng_digits = "0123456789"
        bn_digits = "০১২৩৪৫৬৭৮৯"
        for i in range(10):
            s = s.replace(eng_digits[i], bn_digits[i])
        return s

    @app.template_filter('time_to_bd')
    def time_to_bd_filter(dt):
        if not dt:
            return ""
        from datetime import timedelta
        # If the datetime is naive, assume it's UTC and add 6 hours for display
        # Note: This is a fallback for existing UTC data
        if dt.tzinfo is None:
            dt = dt + timedelta(hours=6)
        return dt.strftime('%d %b, %H:%M')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', password='password123')
            db.session.add(admin)
            db.session.commit()
            
        # Create default product settings if not exists
        if not ProductSetting.query.first():
            setting = ProductSetting(
                product_name="প্রিমিয়াম হানি নাট",
                product_description="খাটি মধু এবং বাছাইকৃত ড্রাই ফ্রুটসের এক অনন্য সংমিশ্রণ। যা আপনাকে দিবে দীর্ঘক্ষণ কাজ করার শক্তি এবং রোগ প্রতিরোধ ক্ষমতা。",
                price=990,
                old_price=1200,
                image_path="honey_nut.png"
            )
            db.session.add(setting)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)