import os
from flask_jwt_extended import JWTManager
from application.constants import HALF_AN_HOUR

def config_jwt(app):
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = HALF_AN_HOUR
    return JWTManager(app)