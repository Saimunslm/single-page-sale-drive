import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from models import db, Order, Admin, ProductSetting, Review, Traffic
from forms import LoginForm, ProductSettingsForm, ShopSettingsForm, ReviewForm
from utils import save_uploaded_file, save_image_as_webp, get_bd_time
import os

# Create blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login route."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.password == form.password.data:
            login_user(admin)
            return redirect(url_for('admin.admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin_login.html', form=form)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard route."""
    orders = Order.query.order_by(Order.timestamp.desc()).all()
    
    # Enrich orders with count of previous orders from same mobile number
    for order in orders:
        order.history_count = Order.query.filter_by(mobile_number=order.mobile_number).count()

    stats = {
        'total': len(orders),
        'pending': Order.query.filter_by(status='Pending').count(),
        'completed': Order.query.filter_by(status='Completed').count()
    }
    
    # Get traffic data for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    traffic_data = Traffic.query.filter(Traffic.timestamp >= thirty_days_ago).all()
    
    # Calculate traffic statistics
    total_visitors = len(traffic_data)
    unique_visitors = len(set([t.ip_address for t in traffic_data if t.ip_address]))
    
    # Get traffic by path
    path_stats = {}
    referrer_stats = {}
    for t in traffic_data:
        # Path stats
        path = t.path or 'Unknown'
        path_stats[path] = path_stats.get(path, 0) + 1
        
        # Referrer stats
        referrer = t.referrer or 'Direct'
        if referrer != 'Direct':
            referrer_stats[referrer] = referrer_stats.get(referrer, 0) + 1
    
    # Sort and get top 5 for each
    top_paths = sorted(path_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    top_referrers = sorted(referrer_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    
    traffic_stats = {
        'total_visitors': total_visitors,
        'unique_visitors': unique_visitors,
        'top_paths': top_paths,
        'top_referrers': top_referrers
    }
    
    # Calculate order statistics for different time periods
    now = datetime.utcnow()
    
    # Daily stats (last 24 hours)
    daily_orders = Order.query.filter(Order.timestamp >= now - timedelta(days=1)).all()
    
    # 7 days stats
    weekly_orders = Order.query.filter(Order.timestamp >= now - timedelta(days=7)).all()
    
    # 14 days stats
    fortnightly_orders = Order.query.filter(Order.timestamp >= now - timedelta(days=14)).all()
    
    # 30 days stats
    monthly_orders = Order.query.filter(Order.timestamp >= now - timedelta(days=30)).all()
    
    # 60 days stats
    two_month_orders = Order.query.filter(Order.timestamp >= now - timedelta(days=60)).all()
    
    # Prepare chart data
    chart_data = {
        'daily': prepare_chart_data(daily_orders, 'daily'),
        'weekly': prepare_chart_data(weekly_orders, 'weekly'),
        'fortnightly': prepare_chart_data(fortnightly_orders, 'fortnightly'),
        'monthly': prepare_chart_data(monthly_orders, 'monthly'),
        'two_month': prepare_chart_data(two_month_orders, 'two_month')
    }
    
    # Calculate traffic statistics for different time periods
    # Daily stats (last 24 hours)
    daily_traffic = Traffic.query.filter(Traffic.timestamp >= now - timedelta(days=1)).all()
    
    # 7 days stats
    weekly_traffic = Traffic.query.filter(Traffic.timestamp >= now - timedelta(days=7)).all()
    
    # 14 days stats
    fortnightly_traffic = Traffic.query.filter(Traffic.timestamp >= now - timedelta(days=14)).all()
    
    # 30 days stats
    monthly_traffic = Traffic.query.filter(Traffic.timestamp >= now - timedelta(days=30)).all()
    
    # 60 days stats
    two_month_traffic = Traffic.query.filter(Traffic.timestamp >= now - timedelta(days=60)).all()
    
    # Prepare traffic chart data
    traffic_chart_data = {
        'daily': prepare_traffic_chart_data(daily_traffic, 'daily'),
        'weekly': prepare_traffic_chart_data(weekly_traffic, 'weekly'),
        'fortnightly': prepare_traffic_chart_data(fortnightly_traffic, 'fortnightly'),
        'monthly': prepare_traffic_chart_data(monthly_traffic, 'monthly'),
        'two_month': prepare_traffic_chart_data(two_month_traffic, 'two_month')
    }
    
    return render_template('admin_dashboard.html', orders=orders, stats=stats, chart_data=chart_data, traffic_stats=traffic_stats, traffic_chart_data=traffic_chart_data)

@admin_bp.route('/admin/product-settings', methods=['GET', 'POST'])
@login_required
def admin_product_settings():
    """Admin product settings route."""
    settings = ProductSetting.query.first()
    form = ProductSettingsForm(obj=settings)
    
    if form.validate_on_submit():
        settings.product_name = form.product_name.data
        settings.price = form.price.data
        settings.old_price = form.old_price.data
        settings.product_description = form.product_description.data
        settings.video_url = form.video_url.data
        settings.product_weight = form.product_weight.data
        settings.discount_amount = form.discount_amount.data
        settings.discount_amount_3 = form.discount_amount_3.data
        
        if form.image.data:
            folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
            filename = save_image_as_webp(form.image.data, folder, prefix='prod')
            if filename:
                settings.image_path = f"uploads/{filename}"
            
        db.session.commit()
        flash('Product settings updated!', 'success')
        return redirect(url_for('admin.admin_product_settings'))
        
    return render_template('admin_product_settings.html', form=form, settings=settings)

@admin_bp.route('/admin/shop-settings', methods=['GET', 'POST'])
@login_required
def admin_shop_settings():
    """Admin shop settings route."""
    # Populate theme choices
    themes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'themes')
    theme_choices = [('default', 'Default')] # Standard fallback
    if os.path.exists(themes_dir):
        themes = [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]
        # Ensure we have a set of unique choices and "default" is one of them
        theme_choices = sorted(list(set([(t, t.capitalize()) for t in themes])))
    
    settings = ProductSetting.query.first()
    form = ShopSettingsForm(obj=settings)
    form.landing_page_theme.choices = theme_choices
    form.thank_you_page_theme.choices = theme_choices
    
    if form.validate_on_submit():
        settings.shop_name = form.shop_name.data
        settings.gtm_id = form.gtm_id.data
        settings.pixel_id = form.pixel_id.data
        settings.support_phone = form.support_phone.data
        settings.whatsapp_number = form.whatsapp_number.data
        settings.facebook_url = form.facebook_url.data
        settings.steadfast_api_key = form.steadfast_api_key.data
        settings.steadfast_secret_key = form.steadfast_secret_key.data
        settings.landing_page_theme = form.landing_page_theme.data
        settings.thank_you_page_theme = form.thank_you_page_theme.data
        settings.custom_head_script = form.custom_head_script.data
        settings.custom_body_script = form.custom_body_script.data
        
        if form.logo.data:
            folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
            filename = save_image_as_webp(form.logo.data, folder, prefix='logo')
            if filename:
                settings.logo_path = f"uploads/{filename}"
            
        db.session.commit()
        flash('Shop settings updated!', 'success')
        return redirect(url_for('admin.admin_shop_settings'))
        
    return render_template('admin_shop_settings.html', form=form, settings=settings)

@admin_bp.route('/admin/reviews', methods=['GET', 'POST'])
@login_required
def admin_reviews():
    """Admin reviews management route."""
    form = ReviewForm()
    if form.validate_on_submit():
        image_path = None
        folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
        
        if form.image.data:
            filename = save_image_as_webp(form.image.data, folder, prefix='rev')
            if filename:
                image_path = f"uploads/{filename}"
            
        profile_pic_path = None
        if form.profile_pic.data:
            filename = save_image_as_webp(form.profile_pic.data, folder, prefix='pfp')
            if filename:
                profile_pic_path = f"uploads/{filename}"
            
        new_review = Review(
            customer_name=form.customer_name.data,
            rating=form.rating.data,
            comment=form.comment.data,
            image_path=image_path,
            profile_pic_path=profile_pic_path
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!', 'success')
        return redirect(url_for('admin.admin_reviews'))
    
    reviews = Review.query.order_by(Review.timestamp.desc()).all()
    return render_template('admin_reviews.html', reviews=reviews, form=form)

@admin_bp.route('/admin/reviews/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    """Edit a review."""
    review = Review.query.get_or_404(review_id)
    form = ReviewForm(obj=review)
    
    if form.validate_on_submit():
        folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
        if form.image.data:
            filename = save_image_as_webp(form.image.data, folder, prefix='rev')
            if filename:
                review.image_path = f"uploads/{filename}"
            
        if form.profile_pic.data:
            filename = save_image_as_webp(form.profile_pic.data, folder, prefix='pfp')
            if filename:
                review.profile_pic_path = f"uploads/{filename}"
            
        review.customer_name = form.customer_name.data
        review.rating = form.rating.data
        review.comment = form.comment.data
        
        db.session.commit()
        flash('Review updated successfully!', 'success')
        return redirect(url_for('admin.admin_reviews'))
        
    return render_template('admin_edit_review.html', form=form, review=review)

@admin_bp.route('/admin/reviews/delete/<int:review_id>')
@login_required
def delete_review(review_id):
    """Delete a review."""
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted!', 'success')
    return redirect(url_for('admin.admin_reviews'))

@admin_bp.route('/admin/order/complete/<int:order_id>')
@login_required
def complete_order(order_id):
    """Mark an order as completed."""
    order = Order.query.get_or_404(order_id)
    order.status = 'Completed'
    db.session.commit()
    flash(f'Order #{order_id} marked as completed.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/order/delete/<int:order_id>')
@login_required
def delete_order(order_id):
    """Delete an order."""
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f'Order #{order_id} deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/order/steadfast-send/<int:order_id>')
@login_required
def admin_send_steadfast(order_id):
    """Send order to SteadFast courier."""
    order = Order.query.get_or_404(order_id)
    settings = ProductSetting.query.first()
    
    if not settings.steadfast_api_key or not settings.steadfast_secret_key:
        flash('SteadFast API keys are not configured.', 'error')
        return redirect(url_for('admin.admin_dashboard'))
    
    # Check if already sent
    if order.steadfast_consignment_id:
        flash(f'Order already sent to SteadFast (CID: {order.steadfast_consignment_id})', 'info')
        return redirect(url_for('admin.admin_dashboard'))

    # Prepare data for SteadFast
    # SteadFast requires 11 digit phone number, removing +88 if exists
    phone = order.mobile_number[-11:] 
    
    payload = {
        "invoice": f"HT-{order.id}",
        "recipient_name": order.full_name,
        "recipient_phone": phone,
        "recipient_address": order.shipping_address,
        "cod_amount": order.total_price,
        "note": f"Qty: {order.quantity}"
    }
    
    headers = {
        "api-key": settings.steadfast_api_key,
        "secret-key": settings.steadfast_secret_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post("https://portal.packzy.com/api/v1/create_order", json=payload, headers=headers, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 200:
            order.steadfast_consignment_id = data['consignment']['consignment_id']
            order.steadfast_status = data['consignment']['status']
            db.session.commit()
            flash(f'Successfully sent to SteadFast! CID: {order.steadfast_consignment_id}', 'success')
        else:
            error_msg = data.get('message') or str(data.get('errors')) or 'Unknown error'
            flash(f'SteadFast Error: {error_msg}', 'error')
    except Exception as e:
        flash(f'Connection Error: {str(e)}', 'error')
        
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/order/steadfast-status/<int:order_id>')
@login_required
def admin_check_steadfast_status(order_id):
    """Check SteadFast delivery status."""
    order = Order.query.get_or_404(order_id)
    settings = ProductSetting.query.first()
    
    if not order.steadfast_consignment_id:
        flash('Order not sent to SteadFast yet.', 'error')
        return redirect(url_for('admin.admin_dashboard'))
        
    headers = {
        "api-key": settings.steadfast_api_key,
        "secret-key": settings.steadfast_secret_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"https://portal.packzy.com/api/v1/status_by_cid/{order.steadfast_consignment_id}", headers=headers, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 200:
            order.steadfast_status = data['delivery_status']
            db.session.commit()
            flash(f'SteadFast Status: {order.steadfast_status}', 'info')
        else:
            flash('Failed to fetch status from SteadFast.', 'error')
    except Exception as e:
        flash(f'Connection Error: {str(e)}', 'error')
        
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/cron/update-steadfast-status')
def cron_update_steadfast_status():
    """Cron job to update SteadFast statuses."""
    # Protection: Add a simple key check if desired, e.g., ?key=your_secret_key
    key = request.args.get('key')
    if key != 'honey-nut-cron-secure-88':
        return "Unauthorized", 401
        
    settings = ProductSetting.query.first()
    if not settings or not settings.steadfast_api_key:
        return "API not configured", 400
        
    # Get orders that are not delivered or cancelled and have a CID
    pending_orders = Order.query.filter(
        Order.steadfast_consignment_id != None,
        ~Order.steadfast_status.in_(['delivered', 'cancelled', 'Delivered', 'Cancelled'])
    ).all()
    
    updated_count = 0
    headers = {
        "api-key": settings.steadfast_api_key,
        "secret-key": settings.steadfast_secret_key,
        "Content-Type": "application/json"
    }
    
    for order in pending_orders:
        try:
            response = requests.get(f"https://portal.packzy.com/api/v1/status_by_cid/{order.steadfast_consignment_id}", headers=headers, timeout=10)
            data = response.json()
            if response.status_code == 200 and data.get('status') == 200:
                order.steadfast_status = data['delivery_status']
                updated_count += 1
        except:
            continue
            
    db.session.commit()
    return f"Processed {len(pending_orders)} orders, Updated {updated_count}.", 200

def prepare_chart_data(orders, period):
    """Prepare chart data based on the time period."""
    now = datetime.utcnow()
    
    if period == 'daily':
        # Group by hour for daily view
        data_points = 24
        interval = timedelta(hours=1)
        labels = [(now - timedelta(hours=i)).strftime('%H:00') for i in range(23, -1, -1)]
    elif period == 'weekly':
        # Group by day for weekly view
        data_points = 7
        interval = timedelta(days=1)
        labels = [(now - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    elif period == 'fortnightly':
        # Group by 2 days for fortnightly view
        data_points = 7
        interval = timedelta(days=2)
        labels = []
        for i in range(12, -1, -2):
            date = now - timedelta(days=i)
            labels.append(date.strftime('%d/%m'))
    elif period == 'monthly':
        # Group by 5 days for monthly view
        data_points = 6
        interval = timedelta(days=5)
        labels = []
        for i in range(25, -1, -5):
            date = now - timedelta(days=i)
            labels.append(date.strftime('%d/%m'))
    elif period == 'two_month':
        # Group by week for two month view
        data_points = 8
        interval = timedelta(weeks=1)
        labels = []
        for i in range(7, -1, -1):
            date = now - timedelta(weeks=i)
            labels.append(date.strftime('%d/%m'))
    
    # Count orders for each time period
    counts = [0] * data_points
    revenues = [0] * data_points
    
    for order in orders:
        if period == 'daily':
            # Calculate hours difference
            diff_hours = int((now - order.timestamp).total_seconds() / 3600)
            if 0 <= diff_hours < 24:
                index = 23 - diff_hours
                counts[index] += 1
                revenues[index] += order.total_price
        elif period == 'weekly':
            # Calculate days difference
            diff_days = (now.date() - order.timestamp.date()).days
            if 0 <= diff_days < 7:
                index = 6 - diff_days
                counts[index] += 1
                revenues[index] += order.total_price
        elif period == 'fortnightly':
            # Calculate 2-day periods difference
            diff_days = (now.date() - order.timestamp.date()).days
            period_index = diff_days // 2
            if 0 <= period_index < 7:
                index = 6 - period_index
                counts[index] += 1
                revenues[index] += order.total_price
        elif period == 'monthly':
            # Calculate 5-day periods difference
            diff_days = (now.date() - order.timestamp.date()).days
            period_index = diff_days // 5
            if 0 <= period_index < 6:
                index = 5 - period_index
                counts[index] += 1
                revenues[index] += order.total_price
        elif period == 'two_month':
            # Calculate week difference
            diff_weeks = int((now.date() - order.timestamp.date()).days / 7)
            if 0 <= diff_weeks < 8:
                index = 7 - diff_weeks
                counts[index] += 1
                revenues[index] += order.total_price
    
    return {
        'labels': labels,
        'counts': counts,
        'revenues': revenues
    }


def prepare_traffic_chart_data(traffic_data, period):
    """Prepare traffic chart data based on the time period."""
    now = datetime.utcnow()
    
    if period == 'daily':
        # Group by hour for daily view
        data_points = 24
        labels = [(now - timedelta(hours=i)).strftime('%H:00') for i in range(23, -1, -1)]
    elif period == 'weekly':
        # Group by day for weekly view
        data_points = 7
        labels = [(now - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    elif period == 'fortnightly':
        # Group by 2 days for fortnightly view
        data_points = 7
        labels = []
        for i in range(12, -1, -2):
            date = now - timedelta(days=i)
            labels.append(date.strftime('%d/%m'))
    elif period == 'monthly':
        # Group by 5 days for monthly view
        data_points = 6
        labels = []
        for i in range(25, -1, -5):
            date = now - timedelta(days=i)
            labels.append(date.strftime('%d/%m'))
    elif period == 'two_month':
        # Group by week for two month view
        data_points = 8
        labels = []
        for i in range(7, -1, -1):
            date = now - timedelta(weeks=i)
            labels.append(date.strftime('%d/%m'))
    
    # Count traffic for each time period
    counts = [0] * data_points
    
    for traffic in traffic_data:
        if period == 'daily':
            # Calculate hours difference
            diff_hours = int((now - traffic.timestamp).total_seconds() / 3600)
            if 0 <= diff_hours < 24:
                index = 23 - diff_hours
                counts[index] += 1
        elif period == 'weekly':
            # Calculate days difference
            diff_days = (now.date() - traffic.timestamp.date()).days
            if 0 <= diff_days < 7:
                index = 6 - diff_days
                counts[index] += 1
        elif period == 'fortnightly':
            # Calculate 2-day periods difference
            diff_days = (now.date() - traffic.timestamp.date()).days
            period_index = diff_days // 2
            if 0 <= period_index < 7:
                index = 6 - period_index
                counts[index] += 1
        elif period == 'monthly':
            # Calculate 5-day periods difference
            diff_days = (now.date() - traffic.timestamp.date()).days
            period_index = diff_days // 5
            if 0 <= period_index < 6:
                index = 5 - period_index
                counts[index] += 1
        elif period == 'two_month':
            # Calculate week difference
            diff_weeks = int((now.date() - traffic.timestamp.date()).days / 7)
            if 0 <= diff_weeks < 8:
                index = 7 - diff_weeks
                counts[index] += 1
    
    return {
        'labels': labels,
        'counts': counts
    }


@admin_bp.route('/admin/logout')
@login_required
def logout():
    """Admin logout route."""
    logout_user()
    return redirect(url_for('admin.admin_login'))