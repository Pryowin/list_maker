import random
import re
from datetime import timezone,date, datetime as dt
from dateutil.relativedelta import relativedelta

from users.models import db, Token, Code
from application.constants import CODE_EXPIRY_SECONDS, MIN_AGE


def write_token(refresh_token: str):
    token = Token(refresh_token=refresh_token, is_valid=True, last_used=dt.now(timezone.utc))
    db.session.add(token)
    db.session.commit()
    return

def write_code(email: str, confirmation_code: str):
    code = Code(email=email, code=confirmation_code)
    db.session.add(code)
    db.session.commit()
    return 

def delete_code(email: str):
    code = Code.query.filter_by(email=email).first()
    db.session.delete(code)
    db.session.commit()

def generate_confirmation_code() -> str:
    return str(random.randint(100000,999999))

def is_ok_to_issue_code(email: str) -> dict:
    code = Code.query.filter_by(email=email).first()
    if code:
        if has_code_expired(code.created_at , CODE_EXPIRY_SECONDS):
            return {"ok":True, "has_expired_code":True}
        else:
            return {"ok":False, "message":"Code already issued"}
    else:
        return {"ok":True, "has_expired_code":False}
    
def has_code_expired(then: dt, expiry_time: int) -> bool:
    duration = dt.now() - then 
    if duration.total_seconds() > expiry_time:
        return True
    else:
        return False
    
def is_user_old_enough(date_of_birth: date) -> bool:
    return user_age(date_of_birth) >= MIN_AGE

def user_age(date_of_birth: date) -> int:
    return (relativedelta(date.today(), date_of_birth)).years

def is_valid_date(date_string)->bool:
    try:
        dt.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def  change_to_date(date_string: str) -> date:
    return dt.strptime(date_string, "%Y-%m-%d")

def is_valid_postal_code(postal_code: str, country: str) -> bool:
    if country == "USA":
        pattern = r'^\d{5}$'
    else:
        # Canada
        pattern = r'^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] [0-9][A-Z][0-9]$'
         
    return re.match(pattern, postal_code) is not None

def is_invalid_email(email: str) -> bool:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return False
    else:
        return True