from flask import Flask

from application.methods import read_field_from_request
from users.models import User, required, unique
from users.methods import change_to_date
from password.methods import encrypt

app = Flask(__name__)

def check_required_fields(request):
    # Check all required fields for user. If all are present return True, otherwise return False and list of missing fields
    errors =[]
    for  field in required:
        value = read_field_from_request(request, field)
        if value is None:
            errors.append(f"'{field}' is required, but is missing from request.")
    
    if errors == []:
        return {"ok": True}
    else:
        return {"ok": False, "errors": errors}
                   
def check_uniqueness(request):
    errors=[]
    for field in unique:
        value = read_field_from_request(request, field)
        check = User.query.filter(getattr(User, field) == value).first()
        if check:
            errors.append(f"{value} already exists for '{field}'.")
            
    if errors == []:
        return {"ok": True}
    else:
        return {"ok": False, "errors": errors}
    
def create(db,request):
    
    phone_formatted = read_field_from_request(request, 'phone')
    phone_unformatted = ''.join([char for char in phone_formatted if char.isdigit()])
    
    user = User(
                user_name = read_field_from_request(request, 'user_name'),
                first_name = read_field_from_request(request, 'first_name'),
                last_name = read_field_from_request(request, 'last_name'),
                email = read_field_from_request(request,'email'),
                phone = phone_unformatted,
                password = encrypt(read_field_from_request(request, 'password')),
                date_of_birth = change_to_date(read_field_from_request(request, 'date_of_birth'))
                )    
    db.session.add(user)
    db.session.commit()
    
