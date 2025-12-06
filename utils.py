import os, secrets
from flask import current_app
from werkzeug.utils import secure_filename
from models import db, Category

def save_picture(form_picture):
    """Renames uploaded image to random hex to avoid collision and saves it."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/products', picture_fn)
    form_picture.save(picture_path)
    return 'products/' + picture_fn

def save_profile_picture(form_picture):
    """Renames profile image and saves it in static/artisans."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(random_hex + f_ext)
    upload_folder = os.path.join(current_app.root_path, 'static/artisans')
    os.makedirs(upload_folder, exist_ok=True)
    picture_path = os.path.join(upload_folder, picture_fn)
    form_picture.save(picture_path)
    return f'artisans/{picture_fn}'

def get_or_create_category(category_name):
    """Standardize category name and create if not exists."""
    clean_name = category_name.strip().title()
    category = Category.query.filter_by(name=clean_name).first()
    if not category:
        category = Category(name=clean_name)
        db.session.add(category)
        db.session.commit()
    return category
