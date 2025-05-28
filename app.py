#app.py
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import CUSTOMER, CUSTOMER_ADDRESSES, CUSTOMER_CONTACTS, DB, ROLE, USER
from flask import Flask, abort, flash, redirect, render_template, request, url_for
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
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))
    
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

@app.route('/customers', methods = ['GET'])
@login_required
def customers():
    #customers_list = CUSTOMER.get_active().all()
    customers_list = DB.session.execute(
        DB.select(
            CUSTOMER.id,
            CUSTOMER.company_name,
            CUSTOMER.gst_number,
            CUSTOMER_ADDRESSES.address_line1,
            CUSTOMER_ADDRESSES.address_line2,
            CUSTOMER_ADDRESSES.address_line3,
            CUSTOMER_CONTACTS.name,
            CUSTOMER_CONTACTS.mobile_number1,
            CUSTOMER_CONTACTS.mobile_number2,
            CUSTOMER_CONTACTS.email,
        )
        .outerjoin(CUSTOMER_ADDRESSES,(CUSTOMER.id == CUSTOMER_ADDRESSES.customer_id)&(CUSTOMER_ADDRESSES.deleted == False)&(CUSTOMER_ADDRESSES.default_address == True))
        .outerjoin(CUSTOMER_CONTACTS,(CUSTOMER.id == CUSTOMER_CONTACTS.customer_id)&(CUSTOMER_CONTACTS.deleted == False)&(CUSTOMER_CONTACTS.default_contact == True))
        .order_by(CUSTOMER.id)
    ).mappings().all()
    return render_template('customers.html',customers_html_var = customers_list)

@app.route('/customer/<int:customer_id>')
@login_required
def customer_detail(customer_id):
    customer = DB.session.execute(
        DB.select(
            CUSTOMER.company_name,
            CUSTOMER.gst_number
        )
        .where(CUSTOMER.id == customer_id)
    ).mappings().all()
    addresses = DB.session.execute(
        DB.select(
            CUSTOMER_ADDRESSES.address_line1,
            CUSTOMER_ADDRESSES.address_line2,
            CUSTOMER_ADDRESSES.address_line3
        )
        .where(CUSTOMER_ADDRESSES.customer_id == customer_id)
    ).mappings().all()
    contacts = DB.session.execute(
        DB.select(
            CUSTOMER_CONTACTS.name,
            CUSTOMER_CONTACTS.mobile_number1,
            CUSTOMER_CONTACTS.mobile_number2,
            CUSTOMER_CONTACTS.email
        )
        .where(CUSTOMER_CONTACTS.customer_id == customer_id)
    ).mappings().all()
    return render_template('customer_detailed.html', customer_html_var =customer, addresses_html_var = addresses, contacts_html_var = contacts)

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST' and "add_customer_hidden_flag" in request.form:

        company_name = request.form.get('company_name_user_ip', '').strip()
        gst_number = request.form.get('gst_number_user_ip', '').strip()

        if not company_name or not gst_number:
            flash('Company name or GST number is empty', 'error')
            return redirect(request.url)

        # Get address and contact inputs
        address_line1_list = request.form.getlist('address_line1[]')
        address_line2_list = request.form.getlist('address_line2[]')
        address_line3_list = request.form.getlist('address_line3[]')

        contact_name_list = request.form.getlist('contact_name[]')
        contact_mobile1_list = request.form.getlist('contact_mobile1[]')
        contact_mobile2_list = request.form.getlist('contact_mobile2[]')
        contact_email_list = request.form.getlist('contact_email[]')

        if not address_line1_list or not contact_name_list:
            flash('At least one address and one contact is required', 'error')
            return redirect(request.url)

        try:
            # Add main customer
            new_customer = CUSTOMER(
                company_name=company_name,
                gst_number=gst_number
            )
            DB.session.add(new_customer)
            DB.session.flush()

            # Add addresses — mark the first one as default
            for idx, (line1, line2, line3) in enumerate(zip(address_line1_list, address_line2_list, address_line3_list)):
                if not line1.strip():
                    continue
                new_address = CUSTOMER_ADDRESSES(
                    customer_id=new_customer.id,
                    address_line1=line1.strip(),
                    address_line2=line2.strip(),
                    address_line3=line3.strip(),
                    default_address=(idx == 0),
                    deleted=False
                )
                DB.session.add(new_address)

            # Add contacts — mark the first one as default
            for idx, (name, mob1, mob2, email) in enumerate(zip(contact_name_list, contact_mobile1_list, contact_mobile2_list, contact_email_list)):
                if not name.strip() or not mob1.strip():
                    continue
                new_contact = CUSTOMER_CONTACTS(
                    customer_id=new_customer.id,
                    name=name.strip(),
                    mobile_number1=mob1.strip(),
                    mobile_number2=mob2.strip(),
                    email=email.strip(),
                    default_contact=(idx == 0),
                    deleted=False
                )
                DB.session.add(new_contact)

            DB.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))

        except Exception as e:
            DB.session.rollback()
            flash(f'Error adding customer: {str(e)}', 'error')

    return render_template('add_customer.html')

#@app.route

if __name__ == '__main__':
    app.run(debug=True)