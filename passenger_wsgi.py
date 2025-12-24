import sys
import os

# Set the path to the application directory
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
# In cPanel, it's better to set these in the "Python App" interface options,
# but setting them here is a safe fallback.
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app object from your main app file
from app import create_app
application = create_app()