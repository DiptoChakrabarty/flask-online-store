import bcrypt 
from app import users

def auth(username,passwd):
    user = users.query.filter_by(username=username).first()
    passwd = passwd.encode('utf-8')

    if bcrypt.checkpw(passwd,user.password) and user:
        return user
    else:
        return "Incorrect"
    
def identity(payload):
    user_id= payload['identity']
    return users.query.filter_by(id=user_id)