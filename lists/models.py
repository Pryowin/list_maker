from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import  Integer, String, DateTime,Date,Boolean
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow

import datetime

from users.models import User

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow(app)

class Category(db.Model):
    category_id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey(User.user_id),nullable=False)
    category_name = Column(String(50))
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    category_creator = relationship('User', foreignkeys='Category.created_by')

class ListHeader(db.Model):
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String(50),nullable=False)
    list_category=Column(Integer, ForeignKey(Category.category_id), nullable=False)
    list_created_by = Column(Integer, ForeignKey(User.user_id),nullable=False)
    list_definition = Column(String,nullable=False)
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    list_creator = relationship('User', foreign_keys='ListHeader.list_created_by')
    category = relationship('Category', foreign_keys='ListHeader.list_category')

class ListItems(db.Model):
    item_id =  Column(Integer, primary_key=True)
    list_id =  Column(Integer, ForeignKey(ListHeader.list_id),nullable=False)  
    list_position = Column(Integer)
    list_item = Column(String, nullable= False)
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    list = relationship('ListHeader', foreign_keys='ListItems.list_id')