import os
from PIL import Image
from utils import save_image_as_webp
import io

folder = 'static/uploads'
for filename in os.listdir(folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')) and 'webp' not in filename:
        path = os.path.join(folder, filename)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        if size_mb > 0.05: # More than 50KB
            print(f"Optimizing {filename} ({size_mb*1024:.2f} KB)...")
            with open(path, 'rb') as f:
                img = Image.open(f)
                if img.mode in ('RGBA', 'P'):
                    # Keep transparency for logos
                    img = img.convert('RGBA')
                
                # Resize to max 400px for logos/small images
                max_width = 800 if 'prod' in filename else 400
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                new_filename = filename.rsplit('.', 1)[0] + "_opt.webp"
                new_path = os.path.join(folder, new_filename)
                img.save(new_path, 'WEBP', quality=75) # Lower quality for speed
                print(f"Created {new_filename}")
