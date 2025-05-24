from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import DB, ROLE, USER
from flask import Flask, flash, redirect, render_template, request
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
    return render_template('index.html')

@app.route('/users_and_roles', methods = ['GET', 'POST'])
@login_required
def users():

    #prevent unauthorised access
    if current_user.role.role_name != 'admin':
        return "Access Denied", 403
    
    #post method to add new user
    if request.method == 'POST':
        #differentiate between add user and add role
        if 'add_user_hidden_flag' in request.form:
            #add new role
            #take input from form
            username = request.form['username_user_ip']
            password = request.form['password_user_ip']
            role_id = request.form['role_id_user_ip']

            #check for repeat username
            """pip install werkzeug bcrypt to get this working"""
            if USER.query.filter_by(username = username).first():
                flash('Username already exists')
            else:
                new_user = USER(
                    username = username,
                    password = generate_password_hash( password, method = "pbkdf2:sha256"),
                    role_id = role_id
                )

                # add and commit the changes
                DB.session.add(new_user)
                DB.session.commit()
                flash('User added successfully')
        # (incomplete) add new user
            
    #get method to get list of usernames and roles
    roles_app_var = ROLE.query.all()
    users_app_var = USER.query.all()

    return render_template('users_and_roles.html', users_html_var = users_app_var, roles_html_var = roles_app_var)

if __name__ == '__main__':
    app.run(debug=True)