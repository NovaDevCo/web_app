from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from forms import RegistrationForm, LoginForm, UserProfileForm, ShopForm, ItemForm
from models import db, User, Shop, Item, Address, Category
from utils import save_picture, save_profile_picture, get_or_create_category  

views_bp = Blueprint('views', __name__, url_prefix='/')

# --- HOME ROUTE ---
@views_bp.route('/')
def home():
    return render_template("base.html") # Or create a home.html


# ---------------------------------------------- AUTHENTICATION ROUTES ---------------------------------------------
# --- LOGIN ---
@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    # FIXED: Use LoginForm, not LoginSeller
    form = LoginForm() 
    
    if form.validate_on_submit():
        # FIXED: Filter by username, not email (matches your User model)
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user:
            flash("Username not found.", "warning")
            return redirect(url_for("views.login"))

        if not user.check_password(form.password.data):
            flash("Incorrect password.", "danger")
        else:
            login_user(user, remember=form.remember_me.data)
            flash(f"Welcome back, {user.first_name}!", "success")
            
            # Redirect logic: Shop or Profile?
            if user.shops:
                # Ensure you have a 'my_shop' route defined later, or change this
                return redirect(url_for("views.my_shop")) 
            return redirect(url_for("views.my_shop")) # Change to profile if needed

    return render_template("login.html", form=form)

# ----------------------------------------------------- LOGOUT --------------------------------------------------------
@views_bp.route('/logout/<int:user_id>')
@login_required
def logout(user_id):
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('views.login'))

# --- SIGNUP ---
@views_bp.route('/signup', methods=['GET', 'POST'])
def sign_up():  
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if username exists
        user_exists = User.query.filter_by(username=form.username.data).first()
        if user_exists:
            flash("Username already exists.", "danger")
            return redirect(url_for('views.sign_up'))

        # Create User only
        new_user = User(
            username=form.username.data,
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for('views.login'))

    return render_template('signup.html', form=form)


# --------------------------------------------- user profile routes -------------------------------------------------------
@views_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    # Display the current user's profile and address.
    user = current_user
    address = user.address  # thanks to one-to-one relationship

    return render_template('profile.html', user=user, address=address)



# The Edit Profile Route
@views_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.gender = form.gender.data
        user.birthdate = form.birthdate.data
        user.contact_num = form.contact_num.data
        user.bio = form.bio.data

        # Handle profile image upload
        if form.profile_image.data:
            user.profile_img_url = save_profile_picture(form.profile_image.data)

        # Handle address
        if user.address:
            user.address.street_address = form.street_address.data
            user.address.city = form.city.data
            user.address.province = form.province.data
            user.address.zip_code = form.zip_code.data
        else:
            new_address = Address(
                user_id=user.user_id,
                street_address=form.street_address.data,
                city=form.city.data,
                province=form.province.data,
                zip_code=form.zip_code.data
            )
            db.session.add(new_address)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.profile'))

    return render_template('edit_profile.html', form=form, user=user)

#_______________________________________________________________________________________________________________
# ------------------------------------ routes related to user created shop -------------------------------------
#_______________________________________________________________________________________________________________
# --- READ: My Shop 
@views_bp.route('/myshop')
@login_required
def my_shop():
    # Ensure user has a shop
    if not current_user.shops:
        return redirect(url_for('views.home')) 
    
    shop = current_user.shops[0] # Getting the first shop
    items = shop.items 
    return render_template('my_shop.html', shop=shop, items=items)


# ------------------------------------------------- create shop route ------------------------------------------
@views_bp.route('/create-shop', methods=['GET', 'POST'])
@login_required
def create_shop():
    # Check if user already has a shop
    if current_user.shops:
        flash("You already have a shop.", "info")
        return redirect(url_for('views.my_shop'))

    form = ShopForm()
    if form.validate_on_submit():
        new_shop = Shop(
            name=form.shop_name.data,
            description=form.shop_description.data,
            owner_id=current_user.user_id
        )
        db.session.add(new_shop)
        db.session.commit()
        flash('Shop created successfully!', 'success')
        return redirect(url_for('views.my_shop'))
    return render_template('create_shop.html', form=form)


# ------------------------------------------------------- CREATE ROUTE -----------------------------------------
@views_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    # ... (shop checks) ...
    form = ItemForm()
    if form.validate_on_submit():
        shop = current_user.shops[0]
        
        # 1. Handle Image (same as before)
        image_file = save_picture(form.image.data) if form.image.data else 'products/default.jpg'

        # 2. Handle Category (String -> Object)
        cat_obj = get_or_create_category(form.category.data)

        new_item = Item(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            img_url=image_file,
            shop_id=shop.shop_id,
            
            # Link to the Category ID we just found/created
            category_id=cat_obj.id 
        )
        
        db.session.add(new_item)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('views.my_shop'))

    return render_template('manage_product.html', form=form, title="Add New Product")


# ----------------------------------------------------- UPDATE ROUTE --------------------------------------------
@views_bp.route('/edit-product/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_product(item_id):
    item = Item.query.get_or_404(item_id)
    # ... (security checks) ...
    form = ItemForm()
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.stock = form.stock.data
        
        # Update Category
        cat_obj = get_or_create_category(form.category.data)
        item.category_id = cat_obj.id
        
        if form.image.data:
            item.img_url = save_picture(form.image.data)
            
        db.session.commit()
        flash('Product updated!', 'success')
        return redirect(url_for('views.my_shop'))
    
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.price.data = item.price
        form.stock.data = item.stock
        
        # PRE-FILL: We need to put the *Name* of the category in the text box
        if item.category:
            form.category.data = item.category.name

    return render_template('manage_product.html', form=form, title="Edit Product")


# ------------------------------------------------- DELETE: Delete Product ------------------------------------
@views_bp.route('/delete-product/<int:item_id>', methods=['POST'])
@login_required
def delete_product(item_id):
    item = Item.query.get_or_404(item_id)
    
    # Security Check
    if item.shop.owner_id != current_user.user_id:
        abort(403)
        
    db.session.delete(item)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('views.my_shop'))




# user shop dashboard
# only user has shop can have a dashboard
# shop dashboard show the shop details, statistic
@views_bp.route('/dashboard')
@login_required
def dashboard():
    shop = current_user.shops[0]

    total_items = db.session.query(func.count(Item.item_id)).filter_by(shop_id=shop.shop_id).scalar()
    total_stock = db.session.query(func.sum(Item.stock)).filter_by(shop_id=shop.shop_id).scalar() or 0
    total_value = db.session.query(func.sum(Item.price * Item.stock)).filter_by(shop_id=shop.shop_id).scalar() or 0

    return render_template(
        'dashboard.html',
        shop=shop,
        total_items=total_items,
        total_stock=total_stock,
        total_value=total_value
    )


