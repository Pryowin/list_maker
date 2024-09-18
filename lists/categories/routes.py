import os

from flask import Flask,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

from application.constants import ADMIN_USER, INCORRECT_DATA, NOT_AUTHORIZED, RECORD_ADDED
from application.methods import read_field_from_request
from lists.models import Category, CategorySchema
from users.models import db, User


category_api = Blueprint('category_api', __name__)

@category_api.route('/lists/categories', methods=['GET'])
@jwt_required(optional=True)
def read_categories():
    current_user = get_jwt_identity()
    if current_user:
        user = User.query.filter_by(email=current_user).first()
        if user:
            user_id = user.user_id
            categories = Category.query.filter((Category.created_by == ADMIN_USER) | (Category.created_by == user_id)).order_by(Category.category_name).all()
        else:
            categories = Category.query.filter(Category.created_by == ADMIN_USER ).order_by(Category.category_name).all()    
    else:
        categories = Category.query.filter(Category.created_by == ADMIN_USER).order_by(Category.category_name).all()
    
    print(categories)
    schema = CategorySchema(many=True)        
    return schema.dump(categories)

@category_api.route('/lists/categories/create', methods=['POST'])
@jwt_required()
def create_category():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message = "Not authorized to add category."), NOT_AUTHORIZED
    
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify(message = "Not authorized to add category."), NOT_AUTHORIZED
    
    category_name = read_field_from_request(request, 'category_name')
    if category_name == "":
        return jsonify(message = "Category cannot be blank."), INCORRECT_DATA
    
    category = Category(created_by = user.user_id, category_name = category_name)
    db.session.add(category)    
    db.session.commit()
    return jsonify(message = "Category added"), RECORD_ADDED
    
        
        

    
