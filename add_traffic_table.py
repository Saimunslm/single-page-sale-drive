from app import create_app
from models import db, Traffic

app = create_app()

with app.app_context():
    # Create only the Traffic table without dropping existing tables
    db.create_all()
    print("Traffic table added successfully without wiping existing data!")