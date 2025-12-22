import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db
from config import config

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.admin_login'
    
    # Import models for login manager
    from models import Admin
    
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
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
            db.session.add(Admin(username='admin', password='password123'))
        # Create default product settings if not exists
        from models import ProductSetting
        if not ProductSetting.query.first():
            db.session.add(ProductSetting(
                product_name="প্রিমিয়াম হানি নাট",
                product_description="খাটি মধু এবং বাছাইকৃত ড্রাই ফ্রুটসের এক অনন্য সংমিশ্রণ। যা আপনাকে দিবে দীর্ঘক্ষণ কাজ করার শক্তি এবং রোগ প্রতিরোধ ক্ষমতা।",
                price=990,
                old_price=1200,
                image_path="honey_nut.png"
            ))
        db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)