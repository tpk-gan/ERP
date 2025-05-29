from models import USER, DB
from werkzeug.security import generate_password_hash

def create_users(admin_role, user_role):
    admin_user = USER(
        username='admin',
        password=generate_password_hash('admin123', method='pbkdf2:sha256'),
        role=admin_role
    )
    user_user = USER(
        username='user',
        password=generate_password_hash('user456', method='pbkdf2:sha256'),
        role=user_role
    )
    DB.session.add_all([admin_user, user_user])
    DB.session.commit()
