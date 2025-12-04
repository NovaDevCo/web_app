from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize DB here to prevent circular imports
db = SQLAlchemy()

# --- NEW ADDRESS TABLE ---
class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True)
    # Foreign Key connecting to User (One-to-One)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    
    street_address = db.Column(db.String(150), nullable=False, default="N/A")
    city = db.Column(db.String(100), nullable=False, default="N/A")
    province = db.Column(db.String(100), nullable=False, default="N/A")
    zip_code = db.Column(db.String(20), nullable=False, default="0000")

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Primary Key
    user_id = db.Column(db.Integer, primary_key=True)
    
    # Auth Data
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Profile Data (Address removed and moved to separate table)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    contact_num = db.Column(db.String(20), nullable=False, default="N/A")
    bio = db.Column(db.Text, nullable=True)
    profile_img_url = db.Column(db.String(250), nullable=True, default='artisans/Althea Ramos.jpg')


    # Relationships
    
    # 1. Address Relationship (One-to-One)
    # uselist=False ensures it behaves like a single object (user.address.city) not a list
    address = db.relationship('Address', backref='user', uselist=False, cascade="all, delete-orphan", lazy=True)

    # 2. Shop Relationship
    shops = db.relationship('Shop', backref='owner', lazy=True)

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Shop(db.Model):
    __tablename__ = 'shops'
    
    shop_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Foreign Key to User
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Self-Referential Key for Branches/Locations
    parent_shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=True)
    
    # Relationship for sub-locations
    sub_locations = db.relationship('Shop', 
                                    backref=db.backref('parent_shop', remote_side=[shop_id]),
                                    lazy=True)

    # One Shop has many items
    items = db.relationship('Item', backref='shop', lazy=True)


class Item(db.Model):
    __tablename__ = 'items'
    
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    img_url = db.Column(db.String(250), nullable=True)

    # Foreign Key to Shop
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False)