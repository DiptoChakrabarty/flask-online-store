import bcrypt 
from model.users import UserModel

def auth(username,password):
    user = UserModel.find_by_username(username)
    password = password.encode('utf-8')
    print(password)

    if UserModel.check_password(username,password):
        return user
    else:
        return None
    
def identity(payload):
    user_id= payload['identity']
    return UserModel.find_by_id(user_id)


    