from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

DB = SQLAlchemy()

class ROLE(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    role_name = DB.Column(DB.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.role_name}>"

class USER(UserMixin, DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256), unique=True, nullable=False)
    password = DB.Column(DB.String(128), nullable=False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('role.id'), nullable=False)
    role = DB.relationship('ROLE', backref='users')
    deleted = DB.Column(DB.Boolean, nullable=False, default=False, index=True)

    def __repr__(self):
        return f"<User {self.username}>"

class CUSTOMER(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    company_name = DB.Column(DB.String(256), unique=True, nullable=False)
    gst_number = DB.Column(DB.String(15), unique=True, nullable=False)
    deleted = DB.Column(DB.Boolean, nullable=False, default=False, index=True)

    #relationships
    addresses = DB.relationship('CUSTOMER_ADDRESSES', backref = 'customer', lazy = 'dynamic', cascade = 'all')
    contacts = DB.relationship('CUSTOMER_CONTACTS', backref = 'customer', lazy = 'dynamic', cascade = 'all')

    # use customer.soft_delete() to use this function
    def soft_delete(self):
        #Soft-delete the customer and its related addresses and contacts.
        self.deleted = True
        for address in self.addresses:
            address.deleted = True
        for contact in self.contacts:
            contact.deleted = True
        DB.session.commit()

    @classmethod
    def get_active(cls):
        return cls.query.filter_by(deleted = False).options(
            DB.joinedload(cls.addresses).filter(CUSTOMER_ADDRESSES.deleted == False).order_by(CUSTOMER_ADDRESSES.id),
            DB.joinedload(cls.contacts).filter(CUSTOMER_CONTACTS.deleted == False).order_by(CUSTOMER_CONTACTS.id)
        )

    def __repr__(self):
        return f"<Customer {self.company_name}>"

class CUSTOMER_ADDRESSES(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    customer_id = DB.Column(DB.Integer, DB.ForeignKey('customer.id'), nullable=False)
    address_line1 = DB.Column(DB.String(256), nullable=False)
    address_line2 = DB.Column(DB.String(256))
    address_line3 = DB.Column(DB.String(256))
    default_address = DB.Column(DB.Boolean, nullable=False, default=False, index=True)
    deleted = DB.Column(DB.Boolean, nullable=False, default=False, index=True)

    def __repr__(self):
        return f"<Address {self.address_line1}: from Company {self.customer.company_name}>"

class CUSTOMER_CONTACTS(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    customer_id = DB.Column(DB.Integer, DB.ForeignKey('customer.id'), nullable=False)
    name = DB.Column(DB.String(256), nullable=False)
    mobile_number1 = DB.Column(DB.String(15), nullable=False)
    mobile_number2 = DB.Column(DB.String(15))
    email = DB.Column(DB.String(254), nullable=False)
    default_contact = DB.Column(DB.Boolean, nullable=False, default=False, index=True)
    deleted = DB.Column(DB.Boolean, nullable=False, default=False, index=True)

    def __repr__(self):
        return f"<Contact {self.name}: from Company {self.customer.company_name}>"