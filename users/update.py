from flask import Flask

from application.methods import read_field_from_request
from users.methods import is_valid_date,is_user_old_enough,change_to_date, is_valid_postal_code, is_invalid_email
from config.methods import is_valid_country, is_valid_region
from application.constants import NOT_AUTHORIZED,INCORRECT_DATA,MIN_AGE

app = Flask(__name__)

def update(db, request, user):
        
    first_name = read_field_from_request(request, 'first_name')
    if first_name is not None:
        user.first_name = first_name
        
    last_name = read_field_from_request(request, 'last_name')
    if last_name is not None:
        user.last_name = last_name    
        
    date_of_birth = request.form.get('date_of_birth', None)
    if date_of_birth is not None:
        user.date_of_birth = change_to_date(date_of_birth)
        
    address_1 = read_field_from_request(request, 'address_1')
    if address_1 is not None:
        user.address_1 = address_1
        
    address_2 = request.form.get('address_2', None)
    if address_2 is not None:
        user.address_2 = address_2
        
    city = request.form.get('city', None)
    if city is not None:
        user.city = city
        
    state = request.form.get('state', None)
    if state is not None:
        user.state = state
        
    zip = request.form.get('zip', None)
    if zip is not None:
        user.zip = zip
        
    db.session.commit()
    
def validate(request, is_create=False) -> dict:
    
    possible_date_of_birth = read_field_from_request(request, 'date_of_birth')
    if possible_date_of_birth:
        if is_valid_date(possible_date_of_birth):
            date_of_birth = change_to_date(possible_date_of_birth)
            if is_user_old_enough(date_of_birth) == False:
                return {"ok": False, "message": f"Must be at least {MIN_AGE} years old to register.", "http_status": NOT_AUTHORIZED} 
        else:
            return {"ok": False, "message": f"'{possible_date_of_birth}' is not a valid date.", "http_status": INCORRECT_DATA} 
    
    
    zip = read_field_from_request(request, 'zip')
    country = read_field_from_request(request, 'country')
    if zip:
        if is_valid_postal_code(zip, country) == False:
            return {"ok": False, "message": f"'{zip}' is not a valid postal code.", "http_status": INCORRECT_DATA} 
        
    if country:
        if is_valid_country(country) == False:
            return {"ok": False, "message": f"'{country}' is not available in this app", "http_status": INCORRECT_DATA}
    
    region = read_field_from_request(request, 'state')
    if region:
        if is_valid_region(country, region) == False:
            return {"ok": False, "message": f"'{region}' is not valid for {country}", "http_status": INCORRECT_DATA}
    
    if is_create:
        email = read_field_from_request(request,'email')
        if is_invalid_email(email):
            return {"ok": False, "message": f"'{email}' is not a valid email address.", "http_status": INCORRECT_DATA} 
        phone = read_field_from_request(request,'phone')
        phone_unformatted = ''.join([char for char in phone if char.isdigit()])
        if len(phone_unformatted) != 10:
            return {"ok": False, "message": f"'{phone}' is not a valid phone number.", "http_status": INCORRECT_DATA} 
        password = read_field_from_request(request,'password')
        password_confirm = read_field_from_request(request,'password_confirm')
        if password != password_confirm:
            return  {"ok": False, "message": "Passwords do not match", "http_status": INCORRECT_DATA}
        
            
    return {"ok": True}