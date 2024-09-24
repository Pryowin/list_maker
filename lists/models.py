import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import  Integer, String, DateTime
from sqlalchemy.orm import relationship

from users.models import db,ma,User


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey('users.user_id'),nullable=False)
    category_name = Column(String(50))
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    category_creator = relationship('User', back_populates='categories')
    lists_in_category = relationship('ListHeader', back_populates='category')

class ListHeader(db.Model):
    __tablename__ = 'list_headers'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String(50),nullable=False)
    list_category=Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    list_created_by = Column(Integer, ForeignKey('users.user_id'),nullable=False)
    list_definition = Column(String,nullable=False)
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    list_creator = relationship('User', back_populates='lists_created_by', foreign_keys=[list_created_by])
    category = relationship('Category', back_populates='lists_in_category', foreign_keys=[list_category])
    
    lists = relationship('ListItem', back_populates='list')

class ListItem(db.Model):
    __tablename__ = 'list_items'
    item_id =  Column(Integer, primary_key=True)
    list_id =  Column(Integer, ForeignKey('list_headers.list_id'),nullable=False)  
    list_position = Column(Integer)
    list_item = Column(String, nullable= False)
    created_at = Column(DateTime,server_default=func.now(datetime.UTC))
    updated_at = Column(DateTime,onupdate=datetime.datetime.now(datetime.UTC))
    
    list = relationship(ListHeader, back_populates='lists', foreign_keys=[list_id])
    
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('category_id','created_by','category_name')
        
category_schema = CategorySchema(many=True)

class ListHeaderSchema(ma.Schema):
    class Meta:
        fields = ('list_id', 'list_name', 'list_category','category_name','list_definition')

    category_name = ma.String(attribute = 'category.category_name')
    
header_schema = ListHeaderSchema()
headers_schema = ListHeaderSchema(many=True)
