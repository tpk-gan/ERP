from models import CUSTOMER, CUSTOMER_ADDRESSES, CUSTOMER_CONTACTS, DB

def create_customers():
    google = CUSTOMER(company_name="Google India", gst_number="29AACCG0527D1Z0")
    address1_c1 = CUSTOMER_ADDRESSES(customer=google, address_line1="No. 3, RMZ Infinity - Tower E", address_line2="Old Madras Road, 4th & 5th Floors, Bangalore,", address_line3="Bangalore, Karnataka, India, 560016.", default_address=True)
    address2_c1 = CUSTOMER_ADDRESSES(customer=google, address_line1="DivyaSree Omega, Survey No. 13,", address_line2="Kondapur Village, Hyderabad,", address_line3="Telangana, 500084, India.")
    contact1_c1 = CUSTOMER_CONTACTS(customer=google, name="google guy", mobile_number1="xxxxxxxxxxxx847", mobile_number2="xxxxxxxxxxxx789", email="googleguy@example.com", default_contact=True)
    contact2_c1 = CUSTOMER_CONTACTS(customer=google, name="google gal", mobile_number1="xxxxxxxxxxxx639", mobile_number2="xxxxxxxxxxxx478", email="googlegal@example.com")

    microsoft = CUSTOMER(company_name="Microsoft Corporation India Pvt. Ltd.", gst_number="06AAACM5586C1ZL")
    address1_c2 = CUSTOMER_ADDRESSES(customer=microsoft, address_line1="Prestige Ferns Galaxy, Sy. No. 7/1, 7/2, 8/1A in Ambalipura,", address_line2="Varthur Hobli, Outer Ring Road,", address_line3="Bengaluru - 560103, Karnataka, India.", default_address=True)
    address2_c2 = CUSTOMER_ADDRESSES(customer=microsoft, address_line1="The Executive Centre, Level 3 B/8, DLF Center,", address_line2="Sansad Marg, Connaught Place, ,", address_line3="New Delhi - 110010, India.")
    contact1_c2 = CUSTOMER_CONTACTS(customer=microsoft, name="microsoft guy", mobile_number1="xxxxxxxxxxxx847", mobile_number2="xxxxxxxxxxxx789", email="microsoftguy@example.com", default_contact=True)
    contact2_c2 = CUSTOMER_CONTACTS(customer=microsoft, name="microsoft gal", mobile_number1="xxxxxxxxxxxx516", email="microsoftgal@example.com")

    DB.session.add_all([google, address1_c1, address2_c1, contact1_c1, contact2_c1])
    DB.session.add_all([microsoft, address1_c2, address2_c2, contact1_c2, contact2_c2])
    DB.session.commit()
