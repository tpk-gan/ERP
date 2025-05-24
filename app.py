from flask_login import LoginManager, login_required, login_user, logout_user
from models import DB, ROLE, USER
from flask import Flask, redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Use a secure random key in production
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Temp.db'
DB.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = USER.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/')
@login_required
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)