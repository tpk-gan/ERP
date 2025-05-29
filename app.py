#app.py
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import CUSTOMER, CUSTOMER_ADDRESSES, CUSTOMER_CONTACTS, DB, ROLE, USER
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from routes.auth import auth_bp
from routes.users import users_bp
from routes.customers import customers_bp

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Use a secure random key in production
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Temp.db'
DB.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(customers_bp)

@app.route('/')
@login_required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)