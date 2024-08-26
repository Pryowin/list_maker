from flask import jsonify,request, Blueprint
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required

from application.constants import RECORD_ADDED, RECORD_UPDATED,NOT_AUTHORIZED, NOT_FOUND, RECORD_EXISTS, INCORRECT_DATA,BAD_PWD_USER, PWD_UPDATED, PWD_NOT_VALID
from application.constants import CODE_EXPIRY_SECONDS
from application.methods import read_field_from_request
from password.methods import encrypt,verify, is_password_valid
from users.methods import write_token,delete_code,has_code_expired
from users.models import db,User,Code


password_api = Blueprint('password_api', __name__)

@password_api.route('/get_token',methods=['POST'])
def get_token():
    password = read_field_from_request(request,'password')
    user_name = read_field_from_request(request,'user_name')
    
    user = User.query.filter_by(user_name=user_name).first()
    
    if user:
        if verify(password, user.password):
             token = create_access_token(user.user_name,fresh=True)
             refresh_token = create_refresh_token(user.user_name)
             write_token(refresh_token)
             return jsonify(message='Token provided', access_token = token, refresh_token = refresh_token)
         
    return jsonify(message='Bad user or password'), NOT_AUTHORIZED


#TODO - Verify token belongs to user
@password_api.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    token = create_access_token(identity, fresh=False)
    return jsonify(message='Token Refreshed', access_token = token)



@password_api.route('/update_password',methods=['POST'])
@jwt_required()
def update_password():
    user_name = read_field_from_request(request,'user_name')
    old_password = read_field_from_request(request,'old_password')
    new_password = read_field_from_request(request,'new_password')
    new_password_retyped = read_field_from_request(request,'new_password_retyped')
    
    if new_password != new_password_retyped:
        return jsonify(message = 'New Passwords do not match.'), INCORRECT_DATA
    
    if get_jwt_identity() != user_name:
        return jsonify(message = "Not authorized"), NOT_AUTHORIZED
    
    user = User.query.filter_by(user_name=user_name).first()
    
    if not user:
        return jsonify(message = BAD_PWD_USER), NOT_AUTHORIZED
    
    if not verify(old_password, user.password):
        return jsonify(message = BAD_PWD_USER), NOT_AUTHORIZED
    
    if is_password_valid(new_password):
        user.password = encrypt(new_password)
        db.session.commit()
        return jsonify(message = PWD_UPDATED), RECORD_UPDATED
    else:
        return jsonify(message = PWD_NOT_VALID), INCORRECT_DATA


@password_api.route('/update_forgotten_password', methods=["POST"])
def update_forgotten_password():
    email = read_field_from_request(request, 'email')        
    new_password = read_field_from_request(request,'new_password')
    new_password_retyped = read_field_from_request(request,'new_password_retyped')
    
    code = read_field_from_request(request,'code')
    check_code = Code.query.filter_by(email=email).first()
    if not check_code:
        return jsonify(message = "Code is not valid."), NOT_AUTHORIZED
    if code != check_code.code:
        return jsonify(message = "Code is not valid."), NOT_AUTHORIZED
    if has_code_expired(check_code.created_at, CODE_EXPIRY_SECONDS):
        return jsonify(message = "Code has expired."), NOT_AUTHORIZED
    if new_password != new_password_retyped:
        return jsonify(message = 'New Passwords do not match.'), INCORRECT_DATA
    if not is_password_valid(new_password):
         return jsonify(message = PWD_NOT_VALID), INCORRECT_DATA
    
    delete_code(email)
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(message = "No user with that email"), INCORRECT_DATA
    else:
        user.password = encrypt(new_password)
        db.session.commit()
        return jsonify(message = PWD_UPDATED), RECORD_UPDATED

    
