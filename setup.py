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
