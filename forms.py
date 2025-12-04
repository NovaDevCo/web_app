from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DecimalField, IntegerField, DateField 
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class UserProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=150)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=150)])
    gender = StringField('Gender', validators=[Optional(), Length(10)])
    birthdate = DateField('Birthdate', format='%Y-%m-%d', validators=[Optional()])
    
    street_address = StringField('Street Address', validators=[Optional(), Length(max=150)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    province = StringField('Province', validators=[Optional(), Length(max=100)])
    zip_code = StringField('Zip Code', validators=[Optional(), Length(max=20)])
    contact_num = StringField('Contact Number', validators=[Optional(), Length(max=20)])
    
    # Use FileField for uploads, not StringField
    profile_image = FileField('Profile Image', validators=[Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only please!')
    ])
    bio = TextAreaField('Bio', validators=[Length(max=500)])

class ShopForm(FlaskForm):
    shop_name = StringField('Shop Name', validators=[DataRequired(), Length(max=150)])
    shop_description = TextAreaField('Description', validators=[Length(max=500)])
    # Logic for sub_location usually handled in backend, but field exists if needed
    sub_location_name = StringField('Branch Location Name', validators=[Length(max=150)])

class ItemForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Available Stock', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    category = StringField('Category', validators=[DataRequired(), Length(max=300)])

    

class Add_to_cart(FlaskForm):
    pass

class Rate_shop(FlaskForm):
    pass