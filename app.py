from flask import Flask
from flask_login import LoginManager
from models import db, User
from views import views_bp
from seed import create_default_shop, seed_shop_items, create_default_user

# Initialize Flask App
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Web_app.db'    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/artisans'

# Initialize Extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(views_bp)

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    with app.app_context():
        # Creates tables based on models.py
        db.create_all() 
        
        # Seed default data
        create_default_user()
        create_default_shop()
        seed_shop_items()

    app.run(debug=True) 