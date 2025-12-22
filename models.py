from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Completed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    steadfast_consignment_id = db.Column(db.String(50), nullable=True)
    steadfast_status = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Order {self.id} - {self.full_name}>'

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class ProductSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False, default="প্রিমিয়াম হানি নাট")
    product_description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=990)
    old_price = db.Column(db.Integer, nullable=False, default=1200)
    image_path = db.Column(db.String(500), nullable=True, default="honey_nut.png")
    logo_path = db.Column(db.String(500), nullable=True)
    gtm_id = db.Column(db.String(50), nullable=True) # e.g. GTM-XXXXXX
    pixel_id = db.Column(db.String(50), nullable=True) # e.g. 123456789
    shop_name = db.Column(db.String(100), nullable=True, default="অর্গানিক দোকান")
    support_phone = db.Column(db.String(20), nullable=True, default="01XXXXXXXXX")
    whatsapp_number = db.Column(db.String(20), nullable=True, default="01XXXXXXXXX")
    facebook_url = db.Column(db.String(200), nullable=True, default="#")
    steadfast_api_key = db.Column(db.String(100), nullable=True)
    steadfast_secret_key = db.Column(db.String(100), nullable=True)
    landing_page_theme = db.Column(db.String(50), nullable=True, default="default")
    thank_you_page_theme = db.Column(db.String(50), nullable=True, default="default")
    video_url = db.Column(db.String(500), nullable=True)
    product_weight = db.Column(db.String(50), nullable=True, default="500")
    discount_amount = db.Column(db.Integer, nullable=True, default=100)
    discount_amount_3 = db.Column(db.Integer, nullable=True, default=200)
    custom_head_script = db.Column(db.Text, nullable=True)
    custom_body_script = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=True) # Optional if photo review
    rating = db.Column(db.Integer, default=5, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(500), nullable=True) # Screenshot/Photo review
    profile_pic_path = db.Column(db.String(500), nullable=True) # Reviewer profile picture
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=True)  # Support IPv6
    user_agent = db.Column(db.Text, nullable=True)
    referrer = db.Column(db.String(500), nullable=True)
    path = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Traffic {self.id} - {self.path}>'
