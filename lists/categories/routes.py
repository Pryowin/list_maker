import os

from flask import Flask,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

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
            user_id = user['user_id']
            categories = Category.query.filter((Category.created_by == 1) | (Category.created_by == user_id)).all()
        else:
            categories = Category.query.filter(Category.created_by ==1 ).all()    
    else:
        categories = Category.query.filter(Category.created_by == 1).all()
    
    print(categories)
    schema = CategorySchema(many=True)        
    return schema.dump(categories)
    
