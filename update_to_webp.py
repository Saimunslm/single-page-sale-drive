from app import create_app
from models import db, ProductSetting
import os

app = create_app()
with app.app_context():
    s = ProductSetting.query.first()
    if s:
        # Find the best existing optimized image
        folder = 'static/uploads'
        optimized_images = [f for f in os.listdir(folder) if f.endswith('_opt.webp')]
        
        prod_img = [f for f in optimized_images if 'prod' in f]
        logo_img = [f for f in optimized_images if 'logo' in f]
        
        if prod_img:
            s.image_path = f"uploads/{prod_img[-1]}"
            print(f"Updated Image to: {s.image_path}")
            
        if logo_img:
            s.logo_path = f"uploads/{logo_img[-1]}"
            print(f"Updated Logo to: {s.logo_path}")
            
        db.session.commit()

