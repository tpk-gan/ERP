from app import app
from models import DB
from sqlalchemy.exc import SQLAlchemyError
from setup.create_roles import create_roles
from setup.create_users import create_users
from setup.create_customers import create_customers

def initialize_database():
    with app.app_context():
        try:
            DB.drop_all()
            DB.create_all()

            admin_role, user_role = create_roles()
            create_users(admin_role, user_role)
            create_customers()

            print("✅ Database initialized successfully.")
        except SQLAlchemyError as e:
            DB.session.rollback()
            print(f"❌ Error initializing database: {str(e)}")
