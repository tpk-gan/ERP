from models import ROLE, DB

def create_roles():
    admin_role = ROLE(role_name='admin')
    user_role = ROLE(role_name='user')
    DB.session.add_all([admin_role, user_role])
    DB.session.commit()
    return admin_role, user_role
