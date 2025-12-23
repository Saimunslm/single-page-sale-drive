import sys
from app import create_app
from models import Admin, ProductSetting


def confirm_reset():
    """Ask user to confirm database reset since it will delete all data."""
    response = input("This will delete all existing data. Are you sure? (yes/no): ")
    return response.lower() in ['yes', 'y']


def main():
    app = create_app()
    
    print("Initializing database...")
    
    if not confirm_reset():
        print("Database reset cancelled.")
        sys.exit(0)
    
    try:
        with app.app_context():
            print("Dropping all collections...")
            # Drop all documents from the collections
            Admin.drop_collection()
            ProductSetting.drop_collection()
            
            print("Creating default records...")
            
            # Re-create admin
            print("Creating admin user...")
            admin = Admin(username='admin', password='password123')
            admin.save()
            
            # Re-create product settings with defaults
            print("Creating default product settings...")
            settings = ProductSetting(
                product_name="প্রিমিয়াম হানি নাট",
                product_description="আমাদের এই হানি নাট বা মধু মিশ্রিত বাদাম সম্পূর্ণ প্রাকৃতিক ও স্বাস্থ্যসম্মত উপায়ে তৈরি।",
                price=990,
                old_price=1200
            )
            settings.save()
            
            print("Database reset successfully with new schema!")
    except Exception as e:
        print(f"Error occurred during database initialization: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()