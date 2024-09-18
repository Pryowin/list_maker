import os

from flask import Flask,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

from application.constants import ADMIN_USER, INCORRECT_DATA, NOT_AUTHORIZED, NOT_FOUND, OK, RECORD_ADDED
from application.methods import read_field_from_request
from lists.models import Category, CategorySchema,ListHeader
from users.models import db, User

header_api = Blueprint('header_api', __name__)

@header_api.route('/lists/headers/create', methods=['POST'])
@jwt_required()
def create_header():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to create list."), NOT_AUTHORIZED
        
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to create list."), NOT_AUTHORIZED
    
    list_created_by = user.user_id
    list_name = read_field_from_request(request, 'list_name')
    list_category = read_field_from_request(request, 'list_category')
    list_definition = read_field_from_request(request, 'list_definition')
    
    if list_name is None:
        return jsonify(message = "List Name is a required field"), INCORRECT_DATA
    
    if list_category is None:
        return jsonify(message = "List Category is a required field"), INCORRECT_DATA
    
    if list_definition is None:
        return jsonify(message = "List Definition is a required field"), INCORRECT_DATA
    
    if type(list_category) != int:
        return jsonify(message = "List Category must be an integer"), INCORRECT_DATA
    
    if type(list_definition) != dict:
        return jsonify(message = "List Category must be a dictionary"), INCORRECT_DATA
    
    header = ListHeader(list_name = list_name, 
                        list_category = list_category, 
                        list_created_by = list_created_by,
                        list_definition = list_definition)
    
    db.session.add(header)
    db.session.commit()
    return jsonify(message = "List Header Created"), RECORD_ADDED
    
        
    
    
    

