from flask import Flask,jsonify, request
from flask_cors import CORS
import logging
import json
import requests
from  flask_socketio import SocketIO, emit
from db import db
from config import DevelopmentConfig

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/response/messages/webhook', methods=['POST'])
def mt4ResponseWebhook():
    response_webhook_data = request.get_json()
    print("Printing the data",response_webhook_data)
    phone = response_webhook_data["phone"]
    socket_name = phone + "bot"
    socketio.emit(socket_name,response_webhook_data, broadcast=True)
    return 'RESPONSE WEBHOOK CALLED'    


@app.route('/request/messages/webhook', methods=['POST'])
def mt4RequestWebhook():
    request_webhook_data = request.get_json()
    print("Printing the data",request_webhook_data)
    phone = request_webhook_data["phone"]
    socket_name = phone + "mt4"
    print('socket_name', socket_name)
    socketio.emit('data',request_webhook_data)
    return 'REQUEST WEBHOOK CALLED'  


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6061)
    # app.run(host='0.0.0.0', port=5000)
