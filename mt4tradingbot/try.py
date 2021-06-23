
from flask import Flask,jsonify
from config import DevelopmentConfig
from db import db
from backend.models import User
import logging
from flask import request

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)


@app.route('/', methods=['GET'])
def main():
    
    return "successful"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060)