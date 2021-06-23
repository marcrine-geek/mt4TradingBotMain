import flask
from flask import Flask, requests, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:marcrine@localhost:5433/mt4TradingBot'
db = SQLAlchemy(app)




app.run()

# REDISTOGO_URL = redis://localhost?db=0
# SESSION = 1BJWap1sBu54arTHBA7j0F1oTsnlGcd_30qTAE_7B8wGX6HlluzolIPJfabTOT0QjsaVzB2WcSIO-FPz420s-X9VUZwiAP5WCm2-C1w8YopZi8PTFHqr20BaAFoZIL1LgiKsjJVaCClL1zGqOlOiXH-QFh5YUji0jw59NBw0poVWM6iLZhsZGGssjoerm-DW3Baau8a59hObV9sfA6yDlojIneCySrKCsTVE3RNFWntJO4qFIgELLBQJV5KlOcIUtMHZu_CYzbCrXICxkSzL9shMoAx0D08Hp7eBuRE-SdMAlkPLJxYgxYQFRdKbSx12FpPuazNWh265TXoeVZ-2Jpmirk1LGm4A=

# "API_ID":"4154197",
# "API_HASH":"17b0517fd71fbff8674d4b43169207a0",
# "CHATINPUT":"https://t.me/joinchat/_uGiN38M4DowODJk",
# "CHATOUTPUT":"@bybitnewybot"

# "email":"marcrinemm22@gmail.com",
#     "password":"marcwere"