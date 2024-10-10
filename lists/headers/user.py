
from flask_jwt_extended import get_jwt_identity

from application.constants import NOT_AUTHORIZED
from users.models import User

def get_user():
    current_user = get_jwt_identity()
    if not current_user:
        return NOT_AUTHORIZED

    user = User.query.filter_by(email=current_user).first()
    if not user:
        return NOT_AUTHORIZED
    
    return user