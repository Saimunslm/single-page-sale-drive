from app import create_app
from models import db, Admin, ProductSetting

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Re-create admin
    admin = Admin(username='admin', password='password123')
    db.session.add(admin)
    
    # Re-create product settings with defaults
    settings = ProductSetting(
        product_name="প্রিমিয়াম হানি নাট",
        product_description="আমাদের এই হানি নাট বা মধু মিশ্রিত বাদাম সম্পূর্ণ প্রাকৃতিক ও স্বাস্থ্যসম্মত উপায়ে তৈরি।",
        price=990,
        old_price=1200
    )
    db.session.add(settings)
    db.session.commit()
    print("Database reset successfully with new schema!")