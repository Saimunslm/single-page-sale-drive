from app import create_app
from models import db, Traffic

app = create_app()

with app.app_context():
    # Check if Traffic table exists
    try:
        # Try to query the Traffic table
        count = db.session.query(Traffic).count()
        print(f"Traffic table exists and contains {count} records")
    except Exception as e:
        print(f"Traffic table does not exist or is not accessible: {e}")