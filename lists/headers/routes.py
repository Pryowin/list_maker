import os

from flask import Flask,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

from application.constants import ADMIN_USER, INCORRECT_DATA, NOT_AUTHORIZED, NOT_FOUND, OK, RECORD_ADDED, RECORD_UPDATED
from application.methods import read_field_from_request
from lists.headers.validations import is_list_definition_valid
from lists.models import Category, CategorySchema,ListHeader, ListItem
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
    
    #TO DO Ensure that list category exists and is valid for this user
    
    if list_name is None:
        return jsonify(message = "List Name is a required field"), INCORRECT_DATA
    
    if list_category is None:
        return jsonify(message = "List Category is a required field"), INCORRECT_DATA
    if type(list_category) != int:
        return jsonify(message = "List Category must be an integer"), INCORRECT_DATA
    
    if list_definition is None:
        return jsonify(message = "List Definition is a required field"), INCORRECT_DATA
    if type(list_definition) != dict:
        return jsonify(message = "List Definition must be a dictionary"), INCORRECT_DATA
    if not is_list_definition_valid(list_definition):
        return jsonify(message = "Invalid List Definition"), INCORRECT_DATA
    
    header = ListHeader(list_name = list_name, 
                        list_category = list_category, 
                        list_created_by = list_created_by,
                        list_definition = list_definition)
    
    db.session.add(header)
    db.session.commit()
    return jsonify(message = "List Header Created"), RECORD_ADDED

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
    
    list = ListHeader.query.filter_by(list_id = read_field_from_request(request, 'list_id'))
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
    
    list_name = read_field_from_request(request, 'list_name')
    list_category = read_field_from_request(request, 'list_category')
    
    list.list_definition = list_definition
    list.list_name = list_name
    list.list_category = list_category
    db.session.update(list)
    db.commit()
    return jsonify(message = 'List Header Updated'),RECORD_UPDATED
    
        
    
    
    

