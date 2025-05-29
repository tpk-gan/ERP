from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from models import DB, ROLE, USER

users_bp = Blueprint('users', __name__)

@users_bp.route('/manage_users', methods = ['GET', 'POST'])
@login_required
def manage_users():

    #prevent unauthorised access
    if current_user.role.role_name != 'admin':
        flash('Access denied','error')
        return render_template('index.html')
    
    #post method to add new user
    if request.method == 'POST':
        #differentiate between add user and add role
        if 'add_user_hidden_flag' in request.form:
            #add new role
            #take input from form
            username = request.form['username_user_ip']
            password = request.form['password_user_ip']
            role_id = request.form['role_id_user_ip']

            if username != None and password != None and role_id != None :
                #check for repeat username
                """pip install werkzeug bcrypt to get this working"""
                if USER.query.filter_by(username = username).first():
                    flash('Username already exists', 'error')
                else:
                    new_user = USER(
                        username = username,
                        password = generate_password_hash( password, method = "pbkdf2:sha256"),
                        role_id = role_id
                    )
                # add and commit the changes
                DB.session.add(new_user)
                DB.session.commit()
                flash('User added successfully','success')
                # (incomplete) add new user
            else:
                flash('One of the required feilds is empty','error')

    #get method to get list of usernames and roles
    roles_app_var = DB.session.execute(DB.select(ROLE)).scalars().all()
    #users_app_var = DB.session.execute(DB.select(USER).where(USER.deleted == False)).scalars().all()
    users_app_var = DB.session.execute(
        DB.select(USER.username,ROLE.role_name)
        .join(ROLE, USER.role_id == ROLE.id)
        .where(USER.deleted == False)
    ).mappings().all()
    #users_app_var = USER.query.filter_by(deleted=False).all()

    return render_template('users_and_roles.html', users_html_var = users_app_var, roles_html_var = roles_app_var)