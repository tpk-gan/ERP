from app import app
from models import DB, ROLE, USER
from werkzeug.security import generate_password_hash

# Run everything inside app context
with app.app_context():
    # Drop and recreate all tables
    DB.drop_all()
    DB.create_all()

    # Create roles
    admin_role = ROLE(role_name='admin')
    DB.session.add(admin_role)
    DB.session.commit()

    # Create default admin user
    admin_user = USER(
        username='admin',
        password=generate_password_hash('admin123'),
        role=admin_role
    )
    DB.session.add(admin_user)
    DB.session.commit()

    print("✅ Database initialized with roles and admin user.")
    print("🔑 Login with username: admin, password: admin123")
