import sqlite3
import os

db_paths = ['instance/orders.db', 'orders.db']

def fix_db(db_path):
    if not os.path.exists(db_path):
        print(f"Skipping {db_path}, not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    columns_to_add = [
        ("landing_page_theme", "TEXT DEFAULT 'default'"),
        ("thank_you_page_theme", "TEXT DEFAULT 'default'"),
        ("video_url", "TEXT"),
        ("product_weight", "TEXT DEFAULT '500'"),
        ("discount_amount", "INTEGER DEFAULT 100"),
        ("discount_amount_3", "INTEGER DEFAULT 200"),
        ("custom_head_script", "TEXT"),
        ("custom_body_script", "TEXT"),
        ("gtm_id", "TEXT"),
        ("pixel_id", "TEXT"),
        ("shop_name", "TEXT DEFAULT 'অর্গানিক দোকান'"),
        ("support_phone", "TEXT DEFAULT '01XXXXXXXXX'"),
        ("whatsapp_number", "TEXT DEFAULT '01XXXXXXXXX'"),
        ("facebook_url", "TEXT DEFAULT '#'"),
        ("steadfast_api_key", "TEXT"),
        ("steadfast_secret_key", "TEXT"),
        ("updated_at", "DATETIME")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE product_setting ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name} to {db_path}")
        except sqlite3.OperationalError:
            print(f"Column {col_name} already exists in {db_path}")
            
    conn.commit()
    conn.close()

for path in db_paths:
    fix_db(path)

print("Database migration completed.")
