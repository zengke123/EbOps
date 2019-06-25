from flask_httpauth import HTTPBasicAuth
from ..models import User


auth = HTTPBasicAuth()
@auth.verify_password
def verify_user(user, password):
    user = User.query.filter(User.username == user).first()
    if not user or not user.verify_password(password):
        return False
    return True
