from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Order, ProductSetting, Review, Traffic

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page route."""
    # Track traffic
    track_traffic(request, '/')
    
    settings = ProductSetting.query.first()
    if not settings:
        # Initial default seeding if none exists
        settings = ProductSetting(
            product_name="প্রিমিয়াম হানি নাট",
            product_description="খাটি মধু এবং বাছাইকৃত ড্রাই ফ্রুটসের এক অনন্য সংমিশ্রণ। যা আপনাকে দিবে দীর্ঘক্ষণ কাজ করার শক্তি এবং রোগ প্রতিরোধ ক্ষমতা।",
            price=990,
            old_price=1200,
            image_path="honey_nut.png"
        )
        db.session.add(settings)
        db.session.commit()
    
    reviews = Review.query.order_by(Review.timestamp.desc()).all()
    theme = settings.landing_page_theme or 'default'
    print(f"DEBUG: Rendering theme: {theme} for shop: {settings.shop_name}")
    return render_template(f'themes/{theme}/index.html', settings=settings, reviews=reviews)

@main_bp.route('/thank-you')
def thank_you():
    """Thank you page after order placement."""
    # Track traffic
    track_traffic(request, '/thank-you')
    
    order_id = request.args.get('order_id')
    order = None
    if order_id:
        order = Order.query.get(order_id)
    
    settings = ProductSetting.query.first()
    theme = settings.thank_you_page_theme or 'default'
    return render_template(f'themes/{theme}/thank_you.html', order=order, settings=settings)

def track_traffic(request, path):
    """Track website traffic."""
    try:
        traffic = Traffic(
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            user_agent=request.headers.get('User-Agent'),
            referrer=request.referrer,
            path=path
        )
        db.session.add(traffic)
        db.session.commit()
    except Exception as e:
        # Log error but don't break the application
        print(f"Error tracking traffic: {e}")
        db.session.rollback()