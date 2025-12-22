from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Order, ProductSetting, Traffic
from utils import convert_to_en_digits, is_valid_bd_mobile
from datetime import datetime

# Create blueprint
orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/order', methods=['POST'])
def place_order():
    """Handle order placement."""
    # Track traffic
    track_traffic(request, '/order')
    
    full_name = request.form.get('full_name')
    address = request.form.get('address')
    mobile = request.form.get('mobile')
    
    # Convert Bengali digits to English digits
    if mobile:
        mobile = convert_to_en_digits(mobile)
        # Remove any spaces or extra characters just in case
        mobile = "".join(mobile.split())
        
    quantity = int(request.form.get('quantity', 1))

    if not full_name or not address or not mobile:
        flash('সবগুলো ঘর পূরণ করুন।', 'error')
        return redirect(url_for('main.index', _anchor='checkout'))

    if not is_valid_bd_mobile(mobile):
        flash('সঠিক বাংলাদেশি মোবাইল নম্বর দিন (১১ ডিজিট)।', 'error')
        return redirect(url_for('main.index', _anchor='checkout'))

    # Anti-spam: Check for recent orders from same number (within 5 mins)
    recent_order = Order.query.filter_by(mobile_number=mobile).order_by(Order.timestamp.desc()).first()
    if recent_order:
        time_diff = datetime.utcnow() - recent_order.timestamp
        if time_diff.total_seconds() < 300: # 5 minutes
            flash('আপনি সম্প্রতি একটি অর্ডার করেছেন। দয়া করে কিছুক্ষণ অপেক্ষা করুন।', 'error')
            return redirect(url_for('main.index', _anchor='checkout'))

    settings = ProductSetting.query.first()
    total_price = settings.price * quantity

    new_order = Order(
        full_name=full_name, 
        shipping_address=address, 
        mobile_number=mobile,
        quantity=quantity,
        total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()
    
    return redirect(url_for('main.thank_you', order_id=new_order.id))

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