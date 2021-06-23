from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class User(BaseClass, db.Model):
    __tablename__="user_details"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    session = db.Column(db.String(1024), unique=True, nullable=True)

    created_on = db.Column(db.DateTime, nullable=True)
    
    def __init__(self,email,password, username, phone, session=None):
        now = datetime.now()
        self.registered_on = now.strftime("%Y-%m-%d %H:%M:%S")
        self.email = email
        self.password = password
        self.username = username
        self.phone = phone
        self.session = session

        

class Inputs(BaseClass, db.Model):
    __tablename__="input_details"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, unique=False, nullable=False)
    chatInput = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))

    def __init__(self, group_id, chatInput,user_id):
        self.group_id = group_id
        self.chatInput = chatInput
        self.user_id = user_id

class Outputs(BaseClass, db.Model):
    __tablename__="output_details"
    id = db.Column(db.Integer, primary_key=True)
    chatOutput = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))

    def __init__(self,chatOutput,user_id):
        self.chatOutput = chatOutput
        self.user_id = user_id



