from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from models import CUSTOMER, CUSTOMER_ADDRESSES, CUSTOMER_CONTACTS, DB

customers_bp = Blueprint('customers',__name__,url_prefix='/customers')

@customers_bp.route('/customer_list', methods = ['GET'])
@login_required
def customer_list():
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

@customers_bp.route('/customer_list/<int:customer_id>')
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

@customers_bp.route('/customer_list/add', methods=['GET', 'POST'])
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
            return redirect(url_for('customers.customer_list'))

        except Exception as e:
            DB.session.rollback()
            flash(f'Error adding customer: {str(e)}', 'error')

    return render_template('add_customer.html')