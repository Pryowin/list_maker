from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime,Date,Boolean,func
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow

import datetime

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(20), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    status = Column(String(1), nullable=False, default='P')
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    categories = relationship('Category', back_populates='category_creator')
    # lists_created_by = relationship('User', back_populates='list_creator')
    lists_created_by = relationship('ListHeader', back_populates='list_creator', foreign_keys='ListHeader.list_created_by')

required=('user_name', 'password', 'first_name', 'last_name', 'date_of_birth', 'email')
unique=('user_name', 'email')

class Token(db.Model):
    __tablename__ = 'tokens'
    refresh_token = Column(String, primary_key=True)
    is_valid = Column(Boolean, default=True)
    last_used = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
class Code(db.Model):
     __tablename__ = 'codes'
     email = Column(String, primary_key=True)
     code = Column(String(6), nullable=False)
     created_at = Column(DateTime,server_default=func.now(datetime.UTC))

class CodeSchema(ma.Schema):
    class Meta:
        fields = ('email', 'code', 'created_at')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id','user_name','password','first_name','last_name','date_of_birth','email','phone',
                  'status', 'created_at', 'updated_at')
        
user_schema = UserSchema()
        
        