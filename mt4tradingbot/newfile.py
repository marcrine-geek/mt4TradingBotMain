from app import copytrade
from backend.models import User
from db import db
from app import app

channel_output = ["@MT4RobotTradingbot"]
channel_input = []

with app.app_context():

    user = db.session.query(User).filter_by(id=11).first()
    usersession = user.username
    phone = user.phone

result = copytrade.delay(usersession, channel_input, channel_output, phone)