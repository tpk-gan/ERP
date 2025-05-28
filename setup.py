from app import app
from models import CUSTOMER, CUSTOMER_ADDRESSES, CUSTOMER_CONTACTS, DB, ROLE, USER
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
#import os

def initialize_database():
    try:
# Run everything inside app context
        with app.app_context():
            # preventing production errors
#            if os.getenv('FLASK_ENV') != 'development':
#                raise RuntimeError("Database wipe only allowed in development")
            
            # Drop and recreate all tables
            DB.drop_all()
            DB.create_all()

            # Create roles
            admin_role = ROLE(role_name='admin')
            user_role = ROLE(role_name='user')
            DB.session.add_all([admin_role,user_role])
            DB.session.commit()

            # Create default admin user
            admin_user = USER(
                username='admin',
                password=generate_password_hash('admin123',  method='pbkdf2:sha256'),
                role=admin_role
            )

            # Create default user user
            user_user = USER(
                username='user',
                password=generate_password_hash('user456',  method='pbkdf2:sha256'),
                role=user_role
            )

            DB.session.add_all([admin_user,user_user])
            DB.session.commit()

            print("✅ Database initialized with roles (admin,user) and (admin user , user user.)")
            print("🔑 Login with username: admin/user, password: admin123/user456")

            # Create default customer
            # All these is info found on internet i neither deny nor accept having any relations with following companies nor do i know if this info is true
            customer1 = CUSTOMER(
                company_name = "Google India",
                gst_number = "29AACCG0527D1Z0"
            )

            address1_c1 = CUSTOMER_ADDRESSES(
                customer = customer1,
                address_line1 = "No. 3, RMZ Infinity - Tower E",
                address_line2 = "Old Madras Road, 4th & 5th Floors, Bangalore,",
                address_line3 = "Bangalore, Karnataka, India, 560016.",
                default_address = True

            )

            address2_c1 = CUSTOMER_ADDRESSES(
                customer = customer1,
                address_line1 = "DivyaSree Omega, Survey No. 13,",
                address_line2 = "Kondapur Village, Hyderabad,",
                address_line3 = "Telangana, 500084, India."
            )

            contact1_c1 = CUSTOMER_CONTACTS(
                customer = customer1,
                name = "google guy",
                mobile_number1 = "xxxxxxxxxxxx847",
                mobile_number2 = "xxxxxxxxxxxx789",
                email = "googleguy@example.com",
                default_contact = True

            )

            contact2_c1 = CUSTOMER_CONTACTS(
                customer = customer1,
                name = "google gal",
                mobile_number1 = "xxxxxxxxxxxx639",
                mobile_number2 = "xxxxxxxxxxxx478",
                email = "googlegal@example.com"
            )

            customer2 = CUSTOMER(
                company_name = "Microsoft Corporation India Pvt. Ltd.",
                gst_number = "06AAACM5586C1ZL"
            )

            address1_c2 = CUSTOMER_ADDRESSES(
                customer = customer2,
                address_line1 = "Prestige Ferns Galaxy, Sy. No. 7/1, 7/2, 8/1A in Ambalipura,",
                address_line2 = "Varthur Hobli, Outer Ring Road,",
                address_line3 = "Bengaluru - 560103, Karnataka, India.",
                default_address = True
            )

            address2_c2 = CUSTOMER_ADDRESSES(
                customer = customer2,
                address_line1 = "The Executive Centre, Level 3 B/8, DLF Center,",
                address_line2 = "Sansad Marg, Connaught Place, ,",
                address_line3 = "New Delhi - 110010, India."
            )
            
            contact1_c2 = CUSTOMER_CONTACTS(
                customer = customer2,
                name = "microsoft guy",
                mobile_number1 = "xxxxxxxxxxxx847",
                mobile_number2 = "xxxxxxxxxxxx789",
                email = "microsoftguy@example.com",
                default_contact = True
            )

            contact2_c2 = CUSTOMER_CONTACTS(
                customer = customer2,
                name = "microsoft gal",
                mobile_number1 = "xxxxxxxxxxxx516",
                email = "microsoftgal@example.com"
            )

            DB.session.add_all([customer1,address1_c1,address2_c1,contact1_c1,contact2_c1])
            DB.session.add_all([customer2,address1_c2,address2_c2,contact1_c2,contact2_c2])
            DB.session.commit()

            print("✅ Customers added with default addresses and contacts")

    except SQLAlchemyError as e:
        DB.session.rollback()
        print(f"❌ Error initializing database: {str(e)}")

if __name__ == "__main__":
    initialize_database()