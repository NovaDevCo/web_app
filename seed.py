# seed.py
from models import db, User, Shop, Item, Address, Category

def create_default_user():
    user = User.query.filter_by(username='@ziagonzales').first()
    if not user:
        new_user = User(
            username='@ziagonzales',
            first_name='Zian',
            last_name='Gonzales',
            contact_num='000-000-0000',
            bio='No bio yet.',
            profile_img_url='artisans/Zia Gonzales.jpg',
            is_admin=True
        )
        new_user.set_password('admin123')
        db.session.add(new_user)
        db.session.commit()

        address = Address(
            user_id=new_user.user_id,
            street_address='232 Mykanto St.',
            city='Biringan City',
            province='East Province',
            zip_code='00000'
        )
        db.session.add(address)
        db.session.commit()
        print("Default User and Address Created.")

def create_default_shop():
    user = User.query.filter_by(username='@ziagonzales').first()
    if user:
        shop = Shop.query.filter_by(owner_id=user.user_id).first()
        if not shop:
            new_shop = Shop(
                name='Zian Clay',
                description='The official default shop.',
                owner_id=user.user_id
            )
            db.session.add(new_shop)
            db.session.commit()
            print("Default Shop Created.")


def seed_shop_items():
    user = User.query.filter_by(username='@ziagonzales').first()
    
    # 1. Try to find the category
    categ = Category.query.filter_by(name='HAND WOOVEN').first()

    if not categ:
        print("Category 'Home & Living' not found. Creating it...")
        categ = Category(name='Wooven')
        db.session.add(categ)
        db.session.commit() # Commit to ensure it has an ID
        
    
    other = Category.query.filter_by(name='Fashion').first()
    if not other:
        other = Category(name='Ceramics')
        db.session.add(other)
        db.session.commit()
    # --- FIX END ---

    if user and user.shops:
        my_shop = user.shops[0]
        
        # Only seed if shop has no items
        if not my_shop.items:
            seed_items = [
                Item(
                    name="Handmade Wooden Bowl", 
                    price=350.00,
                    description="Crafted from local mahogany.",
                    shop_id=my_shop.shop_id, 
                    stock=10,
                    category=categ,  # Now guaranteed to exist
                    img_url='products/1.1.jpg'
                ),
                Item(
                    name="Woven Artisan Bag", 
                    price=1200.00,
                    description="Eco-friendly handwoven bag.",
                    shop_id=my_shop.shop_id, 
                    stock=5,
                    category=other, 
                    img_url='products/1.2.jpg'
                ),
                Item(
                    name="Ceramic Coffee Mug", 
                    price=250.00,
                    description="Hand-painted ceramic mug.",
                    shop_id=my_shop.shop_id, 
                    stock=20,
                    category=other, 
                    img_url='products/1.3.jpg'
                ),
                Item(
                    name="Ceramic Coffee Mug", 
                    price=250.00,
                    description="Hand-painted ceramic mug.",
                    shop_id=my_shop.shop_id, 
                    stock=20,
                    category=other, 
                    img_url='products/1.4.jpg'
                ),
                Item(
                    name="Ceramic Coffee Mug", 
                    price=250.00,
                    description="Hand-painted ceramic mug.",
                    shop_id=my_shop.shop_id, 
                    stock=20,
                    category=other, 
                    img_url='products/1.5.jpg'
                ), 
                Item(
                    name="Ceramic Coffee Mug", 
                    price=250.00,
                    description="Hand-painted ceramic mug.",
                    shop_id=my_shop.shop_id, 
                    stock=20,
                    category=other, 
                    img_url='products/1.5.jpg'
                ),                 
            ]
            db.session.add_all(seed_items)
            db.session.commit()
            print("✅ Default Items Seeded for zian user only.")
        else:
            print("Items already exist for this shop. Skipping.")