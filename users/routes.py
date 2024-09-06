import os

from flask import Flask,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_mail import Mail, Message

from application.methods import read_field_from_request
from application.constants import RECORD_ADDED, RECORD_UPDATED,NOT_AUTHORIZED, NOT_FOUND, RECORD_EXISTS,INCORRECT_DATA, NOT_IMPLEMENTED

from users.models import db,User, UserSchema
from users.methods import delete_code,write_code,generate_confirmation_code,is_ok_to_issue_code
from users.update import update, validate
from users.create import check_required_fields, check_uniqueness, create


# Mail server config
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

user_api = Blueprint('user_api', __name__)

@user_api.route('/create_user', methods=['POST'])
def create_user():
    check = check_required_fields(request)
    if check["ok"] == False:
        return jsonify(check['errors']),INCORRECT_DATA
    
    check = check_uniqueness(request)
    if check["ok"] == False:
        return jsonify(check['errors']),RECORD_EXISTS
    
    validate_result = validate(request,True)
    
    if validate_result["ok"]:
        create(db, request)
        return jsonify(message = "User added"), RECORD_ADDED
    else:
        return jsonify(message = validate_result['message']), validate_result['http_status']
    
@user_api.route('/read_user', methods=['GET'])
@jwt_required()
def read_user():
    email = read_field_from_request(request, 'email')
    if get_jwt_identity() != email:
        return jsonify(message = "Not authorized to access this user."), NOT_AUTHORIZED
    user = User.query.filter_by(email=email).first()
    if user:
        schema = UserSchema(exclude=("password","created_at", "updated_at"))
        unformatted_result = schema.dump(user)
        result = format_for_read(unformatted_result)
        return result
    else:
        return jsonify(message = "User not found"), NOT_FOUND
    


@user_api.route('/update_user',methods=['PUT'])
@jwt_required()
def update_user():
    user_id = read_field_from_request(request, 'user_id')
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify(message = "User not found"), NOT_FOUND
    
    if get_jwt_identity() != user.email:
        app.logger.info(f"Server expects '{get_jwt_identity()}' API supplied '{user.email}'")
        return jsonify(message = "Not authorized to update this user."), NOT_AUTHORIZED
        
    validate_result = validate(request)
    if validate_result["ok"]:
        update(db, request,user)
        return jsonify(message = "User updated"), RECORD_UPDATED
    else:
        return jsonify(message = validate_result["message"]), validate_result["http_status"]
    
@user_api.route('/delete_user', methods=['POST'])
@jwt_required()
def delete_user():
    return jsonify(message = "Users cannot be deleted"), NOT_IMPLEMENTED
    

@user_api.route('/email_confirmation_code',methods=['POST'])
def email_confirmation_code():
    if request.is_json:
        email = request.json['email']
    else:
        email = request.form['email']
        
    check_email = User.query.filter_by(email=email).first()
     
    if check_email:
        check = is_ok_to_issue_code(email)
        if check["ok"]:
            if check["has_expired_code"]:
                delete_code(email)
            code = generate_confirmation_code()
            message = Message("Your confirmation code is : " + code  , 
                           sender='admin@connections.com', 
                           recipients= [email]
                           )
            mail.send(message)
            write_code(email, code)
        else:
            return jsonify(message="A confirmation request is pending"),RECORD_EXISTS
        
    return jsonify(message='If that email exists in our system a code has been sent.')
    
# End of Routes

