import bcrypt 
from model.users import UserModel

def auth(username,passwd):
    user = UserModel.find_by_username(username)
    passwd = passwd.encode('utf-8')

    if userModel.checkpassword(username,password):
        return user
    else:
        return None
    
def identity(payload):
    user_id= payload['identity']
    return UserModel.find_by_id(user_id)


    