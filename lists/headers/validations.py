from ast import literal_eval

from application.constants import (ADMIN_USER, INCORRECT_DATA, NOT_FOUND,
                                   VALID_TYPES)
from lists.models import Category


def is_list_definition_valid(list_definition: dict) -> bool:
    """Returns false if any of the column definitions are invalid"""

    is_string_present = False
    
    if list_definition == {}:
        return False
    
    is_valid = True
    for data_typ in list_definition.values():
        if data_typ not in VALID_TYPES:
            is_valid = False
        else:
            if data_typ == "String":
                is_string_present = True
            
    if not is_string_present:
        is_valid = False
        
    return is_valid

def is_category_valid(user_id: int, category_id: int) -> bool:
    """Returns true if the category exists and it is either a default one created by admin user, or if it is created by the current user"""
    category = Category.query.filter_by(category_id=category_id).first()
    
    if not category:
        return False
    
    if (category.created_by == ADMIN_USER) | (category.created_by == user_id):
        return True
    
    return False

def validate_category(list_category, list_created_by):
    """List category must exist, be an integer, and be available to the current user"""
    if list_category is None:
        return {"ok": False, "message": "List Category is a required field", "return_code": INCORRECT_DATA}
        
    if list_category.isdigit():
        list_category_int = int(list_category)
    else:
        return {"ok": False, "message": "List Category must be an integer", "return_code": INCORRECT_DATA}
    if not is_category_valid(list_created_by, list_category_int):
        return {"ok": False, "message": "List Category does not exist", "return_code": NOT_FOUND}
   
    return {"ok": True}

def validate_definition(list_definition):
    """Returns true if list definition is a dictionary with valid values for all keys"""
    if list_definition is None:
        return {"ok": False, "message": "List Definition is a required field", "return_code": INCORRECT_DATA}
       
    try: 
        list_definition_dict = literal_eval(list_definition)
    except ValueError:
        return {"ok": False, "message": "List Definition must be a dictionary", "return_code": INCORRECT_DATA}
    
    if not is_list_definition_valid(list_definition_dict):
        return {"ok": False, "message": "Invalid List Definition", "return_code": INCORRECT_DATA}
    
    return {"ok": True}

    