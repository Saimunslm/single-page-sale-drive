import re
import os
from werkzeug.utils import secure_filename
from PIL import Image
import io
from datetime import datetime, timedelta, timezone

def get_bd_time():
    """Returns current time in Bangladesh (UTC+6)"""
    return datetime.now(timezone(timedelta(hours=6)))

def convert_to_en_digits(text):
    """
    Convert Bengali digits to English digits.
    
    Args:
        text (str): Text containing Bengali digits
        
    Returns:
        str: Text with English digits
    """
    if not text: 
        return text
    bn_digits = "০১২৩৪৫৬৭৮৯"
    en_digits = "0123456789"
    # Create a mapping table
    table = str.maketrans(bn_digits, en_digits)
    return text.translate(table)

def is_valid_bd_mobile(number):
    """
    Validate Bangladeshi mobile number format.
    
    Args:
        number (str): Mobile number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return bool(re.match(r'^01[3-9]\d{8}$', number))

def save_uploaded_file(file, folder, prefix=''):
    """
    Save an uploaded file with a secure filename.
    
    Args:
        file (FileStorage): Uploaded file object
        folder (str): Destination folder path
        prefix (str): Prefix for the filename
        
    Returns:
        str: Saved filename or None if failed
    """
    if not file:
        return None
        
    try:
        filename = secure_filename(file.filename)
        timestamp = int(get_bd_time().timestamp())
        filename = f"{prefix}_{timestamp}_{filename}"
        file.save(os.path.join(folder, filename))
        return filename
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def save_image_as_webp(file, folder, prefix='', max_width=1200):
    """
    Save an uploaded image as WebP format.
    """
    if not file:
        return None
        
    try:
        # Generate clean filename
        timestamp = int(get_bd_time().timestamp())
        filename = f"{prefix}_{timestamp}.webp"
        filepath = os.path.join(folder, filename)
        
        # Open image with Pillow
        img = Image.open(file)
        
        # Convert to RGB if necessary (rgba to rgb)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Resize if too large (optimization)
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
        # Save as WebP
        img.save(filepath, 'WEBP', quality=85)
        return filename
    except Exception as e:
        print(f"Error converting to webp: {e}")
        return None

