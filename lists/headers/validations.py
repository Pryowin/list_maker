from application.constants import ADMIN_USER, VALID_TYPES
from lists.models import Category


def is_list_definition_valid(list_definition: dict) -> bool:
    
    is_string_present = False
    
    if list_definition == {}:
        return False
    
    is_valid = True
    for type in list_definition.values():
        if type not in VALID_TYPES:
            is_valid = False
        else:
            if type == "String":
                is_string_present = True
            
    if not is_string_present:
       is_valid = False
        
    return is_valid

def is_category_valid(user_id: int, category_id: int) -> bool:
    category = Category.query.filter_by(category_id=category_id).first()
    
    if not category:
        return False
    
    if (category.created_by == ADMIN_USER) | (category.created_by == user_id):
        return True
    
    return False
    