from mongoengine import Document, StringField, IntField, DateTimeField, connect
from flask_login import UserMixin
from datetime import datetime

# No global db object needed for mongoengine, but we can stick to conventions if we want
# or just inherit from Document directly.

class Order(Document):
    full_name = StringField(required=True, max_length=100)
    shipping_address = StringField(required=True)
    mobile_number = StringField(required=True, max_length=20)
    quantity = IntField(default=1)
    total_price = IntField(required=True)
    status = StringField(default='Pending', max_length=20) # Pending, Completed
    timestamp = DateTimeField(default=datetime.utcnow)
    steadfast_consignment_id = StringField(max_length=50)
    steadfast_status = StringField(max_length=50)

    meta = {'indexes': ['-timestamp', 'mobile_number']}

    def __repr__(self):
        return f'<Order {self.id} - {self.full_name}>'

class Admin(UserMixin, Document):
    username = StringField(required=True, unique=True, max_length=80)
    password = StringField(required=True, max_length=120)

    # Required for Flask-Login with MongoDB (ObjectId as string)
    def get_id(self):
        return str(self.id)

class ProductSetting(Document):
    product_name = StringField(required=True, default="প্রিমিয়াম হানি নাট", max_length=200)
    product_description = StringField(required=True, default="খাটি মধু এবং বাছাইকৃত ড্রাই ফ্রুটসের এক অনন্য সংমিশ্রণ। যা আপনাকে দিবে দীর্ঘক্ষণ কাজ করার শক্তি এবং রোগ প্রতিরোধ ক্ষমতা।")
    price = IntField(required=True, default=990)
    old_price = IntField(required=True, default=1200)
    image_path = StringField(default="honey_nut.png", max_length=500)
    logo_path = StringField(max_length=500)
    gtm_id = StringField(max_length=50)
    pixel_id = StringField(max_length=50)
    shop_name = StringField(default="অর্গানিক দোকান", max_length=100)
    support_phone = StringField(default="01XXXXXXXXX", max_length=20)
    whatsapp_number = StringField(default="01XXXXXXXXX", max_length=20)
    facebook_url = StringField(default="#", max_length=200)
    steadfast_api_key = StringField(max_length=100)
    steadfast_secret_key = StringField(max_length=100)
    landing_page_theme = StringField(default="default", max_length=50)
    thank_you_page_theme = StringField(default="default", max_length=50)
    video_url = StringField(max_length=500)
    product_weight = StringField(default="500", max_length=50)
    discount_amount = IntField(default=100)
    discount_amount_3 = IntField(default=200)
    custom_head_script = StringField()
    custom_body_script = StringField()
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'indexes': ['-updated_at']}
    
    # Auto update timestamp
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(ProductSetting, self).save(*args, **kwargs)

class Review(Document):
    customer_name = StringField(max_length=100)
    rating = IntField(default=5)
    comment = StringField()
    image_path = StringField(max_length=500)
    profile_pic_path = StringField(max_length=500)
    timestamp = DateTimeField(default=datetime.utcnow)
    
    meta = {'indexes': ['-timestamp']}

class Traffic(Document):
    ip_address = StringField(max_length=45)
    user_agent = StringField()
    referrer = StringField(max_length=500)
    path = StringField(max_length=500)
    timestamp = DateTimeField(default=datetime.utcnow)
    
    meta = {'indexes': ['-timestamp', 'path', 'timestamp']}
    
    def __repr__(self):
        return f'<Traffic {self.id} - {self.path}>'
