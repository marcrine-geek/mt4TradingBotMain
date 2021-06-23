import os

import json
from dotenv import load_dotenv
load_dotenv()

# chinput = os.getenv('CHATINPUT')
# channel_input = [i for i in chinput.split(' ')] 
# choutput = os.getenv('CHATOUTPUT')


REDISTOGO_URL = "redis://localhost?db=0"

api_id = 4154197
api_hash = "17b0517fd71fbff8674d4b43169207a0"


# postgres_local_base = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
#         user=os.environ.get('FLASK_DATABASE_USER', 'mt4trading'),
#         password=os.environ.get('FLASK_DATABASE_PASSWORD', 'mt4tradingbot'),
#         host=os.environ.get('FLASK_DATABASE_HOST', '127.0.0.1'),
#         port=os.environ.get('FLASK_DATABASE_PORT', 5432),
#         db_name=os.environ.get('FLASK_DATABASE_NAME', 'mt4tradingbot'),
#     )

postgres_local_base = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
        user=os.environ.get('FLASK_DATABASE_USER', 'mt4tradingbot'),
        password=os.environ.get('FLASK_DATABASE_PASSWORD', 'mt4tradingbot'),
        host=os.environ.get('FLASK_DATABASE_HOST', '127.0.0.1'),
        port=os.environ.get('FLASK_DATABASE_PORT', 5432),
        db_name=os.environ.get('FLASK_DATABASE_NAME', 'mt4tradingbot'),
    )



# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'marcrine')
    DEBUG = False
    TOKEN_EXPIRE_HOURS = (24 * 365)

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
