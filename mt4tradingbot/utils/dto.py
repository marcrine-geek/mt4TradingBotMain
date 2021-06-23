from flask_restx import Namespace, fields

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'username': fields.String(required=True, description='user username'),
        'phone': fields.String(required=True, description='user phone')

    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    auth = api.model('auth', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class InputDto:
    api = Namespace('inputData', description='authentication related operations')
    inputData = api.model('inputData', {
        'chatInput': fields.String(required=True, description='The groups links '),

    })

class OutputDto:
    api = Namespace('outputData', description='authentication related operations')
    outputData = api.model('outputData', {
        'chatOutput': fields.String(required=True, description='The telegram main bot '),

    })

class CodeDto:
    api = Namespace('codeData', description='authentication related operations')
    outputData = api.model('codeData', {
        'code': fields.String(required=True, description='The telegram main bot '),
        'phone': fields.String(required=True, description='The telegram main bot '),
    })