from flask import Blueprint

# Create blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return "OK", 200