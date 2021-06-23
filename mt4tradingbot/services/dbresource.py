from backend.models import User, Inputs, Outputs
from db import db 

def chatInputs(user_id):
    chatInputs = db.session.query(Inputs).filter_by(user_id=user_id).first()
    print("_______________---------------------------", chatInputs)
    return chatInputs.chatInput

def chatOutputs(user_id):
    chatOuputs = db.session.query(Outputs).filter_by(user_id=user_id).first()
    print("___________--------------------------", chatOuputs)

    return chatOuputs.chatOutput

def getUserGroups(user_id):
    
    records = db.session.query(Inputs).filter_by(user_id = user_id).all() 
    if records is None:
        print("No chat inputs")

    else:
        print("---------id", User.id)
        print("inputs--------------------", records)
        chat_input = []
        for i in records:
            dictionary = {"chatInput": i.chatInput, "id": i.id}
            chat_input.append(id)
    
    return chat_input

def getSession(email):
    session = db.session.query(User).filter_by(email=email).first()
    return session.session