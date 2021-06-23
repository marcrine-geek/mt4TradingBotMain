from backend.models import User, Inputs, Outputs
from flask_restx import Resource, abort
from flask import request
import jwt
import re
import datetime
import functools
from flask import make_response, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
import config
from time import gmtime, strftime
from db import db
from flask import current_app as app

from utils.dto import UserDto
from utils.dto import InputDto
from utils.dto import OutputDto

from redistasks import copytrade

from services import dbresource


from utils.dto import AuthDto
import json



from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

session = User.username

api = UserDto.api
user = UserDto.user

def login_required(method):
    @functools.wraps(method)
    def wrapper(self):
        header = request.headers.get('Authorization')
        _, token = header.split()
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.DecodeError:
            return {'message':'Token is not valid.', 'status':400}
        except jwt.ExpiredSignatureError:
            return {'message':'Token is expired.', 'status': 400}
        email = decoded['email']
        if len(User.query.filter_by(email = email).all()) == 0:
            return {'message':'User is not found.', 'status':400}
        user = User.query.filter_by(email = email).all()[0]
        return method(self, user)
    return wrapper


@api.route('/register')
class Register(Resource):
    
    @api.doc('register a user')
    @api.expect(user, validate=True)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        username = request.json['username']
        phone = request.json['phone']

        
        user = User.query.filter_by(email = email).all()
        if not user:
            if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email):
                return {'message':'email is not valid.','status':400}
            if len(password) < 6:
                return {'message':'password is too short.','status':400}

            User.query.filter_by(email = email).all()

            if len(User.query.filter_by(email = email).all()) != 0:
                return {'message':'email is already used.', 'status':400}
            else:
                user = User(email= email, password =generate_password_hash(password), username=username, phone=phone)
                db.session.add(user)
                db.session.commit()
            

            return {'email': email,'message':'user successfully registered','status':201}
        else:
            return {"message":"Unauthorized user", "status":400}


api2 = AuthDto.api
auth = AuthDto.auth

@api.route('/login')
class Login(Resource):
    @api.doc('Login a user')
    @api.expect(auth, validate=True)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        
        if len(User.query.filter_by(email = email).all()) == 0:
            return {'message':'User is not found.','status':400}
        user = User.query.filter_by(email = email).first()
        if user:
            print("--------------------------user------------------------\n", user)
            
            if not check_password_hash(user.password, password):
                return {'message':'Password is incorrect.', 'status':400}
            print("here here here")
            exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
            print("________________________________________")
            encoded = jwt.encode({'email': email,'userid':user.id, 'exp': exp}, app.config['SECRET_KEY'], algorithm='HS256')
            print("-----------------------------------------")

            return { 'message':'login sucessfully', 'email': email, 'token': encoded,'phone': user.phone, 'status':200}
        else:
            return {"message":"Unauthorized user", "status":400}


api4 = InputDto.api
inputData = InputDto.inputData           
@api.route('/add/groups')
class ChatInput(Resource):
    @login_required
    def post(self, user):
        
        data = request.json['data']
        record = []
        
        for i in range(len(data)):
            print("------------------", data[i]["id"])
            i = Inputs(group_id = data[i]["id"], chatInput = data[i]["title"], user_id = user.id)
            record.append(i)
        db.session.add_all(record) 
        db.session.commit() 
        records = db.session.query(Inputs).filter_by(user_id = user.id).first()  
        print("__________________________", record)
        
        return {"message":"Groups added successfully"}, 200
      

@api.route('/groups/list')
class ChatInputDetails(Resource):
    @login_required
    def post(self, user):
        records = db.session.query(Inputs).filter_by(user_id = user.id).all() 
        if records is None:
            return {'message':'No chat inputs'}

        else:
            outputs = db.session.query(Outputs).filter_by(user_id = user.id).all()
            if outputs is None:
                return {'message':'No chat outputs'}

            else:
                output_store =[]
                for i in outputs:
                    output_store.append(i.chatOutput)
        
            print("---------id", user.id)
            print("inputs--------------------", records)
            input_store = []
            for i in records:
                dictionary = {"chatInput": i.chatInput, "id": i.group_id}
                input_store.append(dictionary)
            chat_inputs = [] 
            chat_outputs = output_store 
            # get Groups
            for chat in input_store:
                group =chat["id"]
                chat_inputs.append(group)
            result = copytrade.delay(user.session, chat_inputs, chat_outputs, user.phone)
            

            return {"message": "chat inputs fetched successfully", "data":input_store}, 200


@api.route('/phone')
class ChatInputDetails(Resource):
    @login_required
    def get(self, user):
        records = db.session.query(User).filter_by(phone = user.phone).first() 
        if records:
            phone = user.phone
            return phone



api5 = OutputDto.api
outputData = OutputDto.outputData 
@api.route('/add/bot')
class ChatOutput(Resource):
    @login_required
    @api.doc('User Output Bot')
    @api.expect(outputData, validate=True)
    def post(self, user):
        chatOutput=request.json['chatOutput']

        apidetas2 = db.session.query(Outputs).filter_by(chatOutput = chatOutput).first()

        if apidetas2 is None:
            apidetas11 = {
                "chatOutput":chatOutput,
                "user_id":user.id
            }
            useroutput = Outputs(**apidetas11)
            db.session.add(useroutput)
            db.session.commit()


            return{'message':'Successfully added.', 'status':200}

        else:
            return{'message':'Upload failed.', 'status':400}

@api.route('/bots/list')
class ChatOutputDetails(Resource):
    @login_required
    def get(self, user):
        outputs = db.session.query(Outputs).filter_by(user_id = user.id).all()
        if outputs is None:
            return {'message':'No chat outputs'}

        else:
            output_store =[]
            for i in outputs:
                output_store.append(i.chatOutput)
            
            
            return {"message": "chat inputs fetched successfully", "data":output_store}, 200


@api.route('/')
class Details(Resource):
    @login_required
    def get(self, user):
        return {"success"}

