from application.constants import VALID_TYPES


def is_list_definition_valid(list_definition: dict) -> bool:
    
    if list_definition == {}:
        return False
    
    is_valid = True
    for type in list_definition.values():
        if type not in VALID_TYPES:
            is_valid = False
            
    return is_valid