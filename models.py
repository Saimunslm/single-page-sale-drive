from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    old_price = db.Column(db.Integer)
    image_path = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False, index=True)
    # items relationship defined backref in OrderItem? Or explicitly here.
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    
    quantity = db.Column(db.Integer, default=1) # Deprecated but kept
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Confirmed, Cancelled, Completed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    steadfast_consignment_id = db.Column(db.String(50))
    steadfast_status = db.Column(db.String(50))

    def __repr__(self):
        return f'<Order {self.id} - {self.full_name}>'

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

class ProductSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False, default="প্রিমিয়াম হানি নাট")
    product_description = db.Column(db.Text, nullable=False, default="খাটি মধু এবং বাছাইকৃত ড্রাই ফ্রুটসের এক অনন্য সংমিশ্রণ। যা আপনাকে দিবে দীর্ঘক্ষণ কাজ করার শক্তি এবং রোগ প্রতিরোধ ক্ষমতা।")
    price = db.Column(db.Integer, nullable=False, default=990)
    old_price = db.Column(db.Integer, nullable=False, default=1200)
    image_path = db.Column(db.String(500), default="honey_nut.png")
    logo_path = db.Column(db.String(500))
    gtm_id = db.Column(db.String(50))
    pixel_id = db.Column(db.String(50))
    shop_name = db.Column(db.String(100), default="অর্গানিক দোকান")
    support_phone = db.Column(db.String(20), default="01XXXXXXXXX")
    whatsapp_number = db.Column(db.String(20), default="01XXXXXXXXX")
    facebook_url = db.Column(db.String(200), default="#")
    steadfast_api_key = db.Column(db.String(100))
    steadfast_secret_key = db.Column(db.String(100))
    landing_page_theme = db.Column(db.String(50), default="default")
    thank_you_page_theme = db.Column(db.String(50), default="default")
    video_url = db.Column(db.String(500))
    product_weight = db.Column(db.String(50), default="500")
    discount_amount = db.Column(db.Integer, default=100)
    discount_amount_3 = db.Column(db.Integer, default=200)
    custom_head_script = db.Column(db.Text)
    custom_body_script = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    rating = db.Column(db.Integer, default=5)
    comment = db.Column(db.Text)
    image_path = db.Column(db.String(500))
    profile_pic_path = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.String(500))
    path = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Traffic {self.id} - {self.path}>'
