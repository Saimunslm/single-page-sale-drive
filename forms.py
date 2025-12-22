from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """Form for admin login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductSettingsForm(FlaskForm):
    """Form for product settings."""
    product_name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    price = IntegerField('Current Price', validators=[DataRequired()])
    old_price = IntegerField('Old Price', validators=[DataRequired()])
    product_description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    video_url = StringField('Product Video URL (YouTube/Vimeo)')
    product_weight = StringField('Product Weight (In Grams, e.g. 500)')
    discount_amount = IntegerField('2-Pack Discount (BDT)', default=100)
    discount_amount_3 = IntegerField('3-Pack Discount (BDT)', default=200)
    submit = SubmitField('Update Product')

class ShopSettingsForm(FlaskForm):
    """Form for shop settings."""
    shop_name = StringField('Shop Name', validators=[DataRequired()])
    logo = FileField('Shop Logo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'svg', 'webp'], 'Images only!')
    ])
    gtm_id = StringField('Google Tag Manager ID (GTM-XXXXXX)')
    pixel_id = StringField('Facebook Pixel ID')
    support_phone = StringField('Support Phone Number')
    whatsapp_number = StringField('WhatsApp Number')
    facebook_url = StringField('Facebook Page URL')
    steadfast_api_key = StringField('SteadFast API Key')
    steadfast_secret_key = StringField('SteadFast API Secret Key')
    
    landing_page_theme = SelectField('Landing Page Theme', choices=[])
    thank_you_page_theme = SelectField('Thank You Page Theme', choices=[])
    
    custom_head_script = TextAreaField('Custom Head Script (Tracking codes, CSS etc.)')
    custom_body_script = TextAreaField('Custom Body Script (Messenger chat, scripts etc.)')
    
    submit = SubmitField('Save Shop Settings')

class ReviewForm(FlaskForm):
    """Form for customer reviews."""
    customer_name = StringField('Customer Name')
    rating = IntegerField('Rating (1-5)')
    comment = TextAreaField('Review Comment')
    image = FileField('Review Photo/Screenshot', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    profile_pic = FileField('Reviewer Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    submit = SubmitField('Add Review')