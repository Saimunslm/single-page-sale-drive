# Organic Dokan - Single Page Sale Drive

A Flask-based e-commerce application for selling organic products with integrated SteadFast courier API.

## Features

- Single page product showcase
- Multiple customizable themes
- Order management system
- SteadFast courier integration
- Customer review system
- Traffic analytics
- Responsive design

## Prerequisites

- Python 3.10 or higher
- MongoDB database
- cPanel hosting account (for deployment)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd organic-dokan
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file with the following variables:
   ```
   FLASK_CONFIG=development
   SECRET_KEY=your-secret-key
   DEV_MONGODB_URI=mongodb://localhost:27017/organic_shop_db
   ```

5. Initialize the database:
   ```
   python init_db.py
   ```

## Deployment on cPanel

1. Upload all files (except `venv` and `__pycache__`) to your cPanel file manager
2. In cPanel, go to "Setup Python App"
3. Click "Create Application"
4. Select Python Version 3.10 or higher
5. Set Application root to your uploaded folder
6. Set Application URL to your domain
7. Set Application startup file to `passenger_wsgi.py`
8. Set Application Entry point to `application`
9. Click "Create"
10. After creation, copy the command shown and run it in cPanel Terminal
11. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
12. Set file permissions:
    - Directories: 755
    - Files: 644
13. Restart the application from the "Setup Python App" section

## Configuration

### Admin Panel Access
- URL: `/admin`
- Default credentials:
  - Username: `admin`
  - Password: `password123`
  
Change these credentials immediately after first login.

### Theme Customization
Themes are located in `templates/themes/`. Each theme has:
- `index.html` - Main landing page
- `thank_you.html` - Order confirmation page

### Product Settings
Configure product details, pricing, and images through the admin panel.

## Troubleshooting

### Common Issues

1. **Internal Server Error (500)**
   - Check cPanel error logs
   - Verify all file permissions (755 for directories, 644 for files)
   - Ensure `passenger_wsgi.py` exists and is configured correctly

2. **Template Not Found**
   - Verify theme directories exist in `templates/themes/`
   - Check that each theme has both `index.html` and `thank_you.html`

3. **Static Files Not Loading**
   - Confirm static files are in the `static/` directory
   - Check that image paths in templates use `url_for('static', filename=...)`

### File Permissions
Ensure correct permissions:
```
find . -type d -exec chmod 755 {} \;  # Directories
find . -type f -exec chmod 644 {} \;  # Files
```

## API Integrations

### SteadFast Courier
1. Obtain API Key and Secret Key from SteadFast
2. Add credentials in Admin Panel → Shop Settings
3. Orders can be sent to SteadFast directly from the admin dashboard

## Support
For issues or questions, contact the development team.