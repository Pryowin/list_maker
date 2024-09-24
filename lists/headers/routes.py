import os

from flask import Flask,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.orm import joinedload

from application.constants import ADMIN_USER, INCORRECT_DATA, NOT_AUTHORIZED, NOT_FOUND, OK, RECORD_ADDED, RECORD_UPDATED
from application.methods import read_field_from_request
from lists.headers.validations import is_category_valid, is_list_definition_valid
from lists.models import ListHeader, ListHeaderSchema, ListItem, header_schema
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
    if list_category.isdigit():
        list_category_int = int(list_category)
    else:
        return jsonify(message = "List Category must be an integer"), INCORRECT_DATA
    if not is_category_valid(list_created_by, list_category_int):
        return jsonify(message = "List Category does not exist"), NOT_FOUND
    
    
    if list_definition is None:
        return jsonify(message = "List Definition is a required field"), INCORRECT_DATA
    
    try: 
        list_definition_dict = eval(list_definition)
    except:
        return jsonify(message = "List Definition must be a dictionary"), INCORRECT_DATA
    
    if not is_list_definition_valid(list_definition_dict):
        return jsonify(message = "Invalid List Definition"), INCORRECT_DATA
    
    header = ListHeader(list_name = list_name, 
                        list_category = list_category_int, 
                        list_created_by = list_created_by,
                        list_definition = list_definition)
    
    db.session.add(header)
    db.session.commit()
    return jsonify(message = "List Header Created"), RECORD_ADDED

@header_api.route('/lists/headers/<int:id>', methods=['GET'])
@jwt_required()  
def read_header(id):
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
            
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
    
    user_id = user.user_id
    list = ListHeader.query.options(joinedload(ListHeader.category)).filter_by(list_id = id).first()
    if not list:
        return jsonify(message = "List does not exist"), NOT_FOUND
    
    if user_id != list.list_created_by:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
    
    # schema = ListHeaderSchema()
    # return schema.dump(list)
    
    return jsonify(header_schema.dump(list)), OK

@header_api.route('/lists/headers/update', methods=['PUT'])
@jwt_required()  
def update_header():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to update list."), NOT_AUTHORIZED
        
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to update list."), NOT_AUTHORIZED
    
    user_id = user.user_id
    
    if list_category is None:
        return jsonify(message = "List Category is a required field"), INCORRECT_DATA
    if list_category.isdigit():
        list_category_int = int(list_category)
    else:
        return jsonify(message = "List Category must be an integer"), INCORRECT_DATA
    if not is_category_valid(user_id, list_category_int):
        return jsonify(message = "List Category does not exist"), NOT_FOUND
    
    list = ListHeader.query.filter_by(list_id = read_field_from_request(request, 'list_id')).first()
    if not list:
        return jsonify(message = "List not found"), NOT_FOUND
    
    if list.created_by != user_id:
        return jsonify(message = "Not authorized to update list."), NOT_AUTHORIZED
    
    
    list_id = read_field_from_request(request, 'list_id')
    list_definition = read_field_from_request(request, 'list_definition')
    if not (list_definition is None):
        if list_definition != list.list_definition:
            if ListItem.query_by(list_id=list_id).count() > 0:
                return jsonify(message = "Unable to change list definition when list items exist."), INCORRECT_DATA
    try: 
        list_definition_dict = eval(list_definition)
    except:
        return jsonify(message = "List Definition must be a dictionary"), INCORRECT_DATA
    if not is_list_definition_valid(list_definition_dict):
        return jsonify(message = "Invalid List Definition"), INCORRECT_DATA
    
    list_name = read_field_from_request(request, 'list_name')
    list_category = read_field_from_request(request, 'list_category')
    
    list.list_definition = list_definition
    list.list_name = list_name
    list.list_category = list_category
    db.session.update(list)
    db.commit()
    return jsonify(message = 'List Header Updated'),RECORD_UPDATED
    
        
    
    
    

