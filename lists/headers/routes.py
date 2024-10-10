import os

from flask import jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.orm import joinedload

from application.constants import INCORRECT_DATA, NOT_AUTHORIZED, NOT_FOUND, OK, RECORD_ADDED
from application.constants import RECORD_UPDATED
from application.methods import read_field_from_request
from lists.headers.validations import validate_category, validate_definition
from lists.models import ListHeader, ListItem, header_schema, headers_schema
from users.models import db, User

header_api = Blueprint('header_api', __name__)

@header_api.route('/lists/headers/create', methods=['POST'])
@jwt_required()
def create_header():
    """Route for creating list header"""
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

    check = validate_category(list_category, list_created_by)
    if not check["ok"]:
        return jsonify(message = check["message"]), check["return_code"]

    check = validate_definition(list_definition)
    if not check["ok"]:
        return jsonify(message = check["message"]), check["return_code"]

    header = ListHeader(list_name = list_name, 
                        list_category = int(list_category),
                        list_created_by = list_created_by,
                        list_definition = list_definition)
    
    db.session.add(header)
    db.session.commit()
    return jsonify(message = "List Header Created"), RECORD_ADDED


@header_api.route('/lists/headers/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_header(id):
    """Route for deleting list header for specified list"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to delete list."), NOT_AUTHORIZED

    user = User.query.filter_by(email=current_user).first()
    if not user:    
        return jsonify(message = "Not authorized to delete list."), NOT_AUTHORIZED
    
    user_id = user.user_id
    list_header = ListHeader.query.options(joinedload(ListHeader.category)).filter_by(list_id = id).first()
    if not list_header:
        return jsonify(message = "List does not exist"), NOT_FOUND
    
    if user_id != list_header.list_created_by:
        return jsonify(message = "Not authorized to delete list."), NOT_AUTHORIZED
    
    db.session.delete(list_header)
    db.session.commit()
    return jsonify(message = "List '"+ list_header.list_name +"' deleted"), OK
    
@header_api.route('/lists/headers/<int:id>', methods=['GET'])
@jwt_required()
def read_header(id):
    """Route for reading list header for specified list"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
            
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
    
    user_id = user.user_id
    list_header = ListHeader.query.options(joinedload(ListHeader.category)).filter_by(list_id = id).first()
    if not list_header:
        return jsonify(message = "List does not exist"), NOT_FOUND
    
    if user_id != list_header.list_created_by:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
       
    return jsonify(header_schema.dump(list_header)), OK


@header_api.route('/lists/headers/', methods=['GET'])
@jwt_required()  
def read_headers():
    """Route for reading all list headers created by current user"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
            
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to read list."), NOT_AUTHORIZED
    
    user_id = user.user_id
    lists = ListHeader.query.options(joinedload(ListHeader.category)).filter_by(list_created_by = user_id).all()
    
    return jsonify(headers_schema.dump(lists)), OK
    
    
@header_api.route('/lists/headers/update', methods=['PUT'])
@jwt_required() 
def update_header():
    """Route for updating list header"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to update list."), NOT_AUTHORIZED
        
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to update list."), NOT_AUTHORIZED
    
    user_id = user.user_id
    list_category = read_field_from_request(request, 'list_category')
    check = validate_category(list_category, user_id)
    if not check["ok"]:
        return jsonify(message = check["message"]), check["return_code"]
    
    list_header = ListHeader.query.filter_by(list_id = read_field_from_request(request, 'list_id')).first()
    if not list_header:
        return jsonify(message = "List not found"), NOT_FOUND
    
    if list_header.list_created_by != user_id:
        return jsonify(message = "Not authorized to update list."), NOT_AUTHORIZED
    
    list_id = read_field_from_request(request, 'list_id')
    list_definition = read_field_from_request(request, 'list_definition')

    check = validate_definition(list_definition)
    if not check["ok"]:
        return jsonify(message = check["message"]), check["return_code"]
      
    if list_definition != list_header.list_definition:
        if ListItem.query_by(list_id=list_id).count() > 0:
            return jsonify(message = "Unable to change list definition when list items exist."), INCORRECT_DATA
    
    list_name = read_field_from_request(request, 'list_name')
    
    list_header.list_definition = list_definition
    list_header.list_name = list_name
    list_header.list_category = list_category
    
    db.session.commit()
    return jsonify(message = 'List Header Updated'),RECORD_UPDATED

