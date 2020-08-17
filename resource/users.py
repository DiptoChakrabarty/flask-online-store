from flask_restful import Resource,reqparse
import bcrypt
from model.users import UserModel

class users(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        passwd = data["password"]
        hashed = bcrypt.hashpw(passwd.encode('utf-8'),bcrypt.gensalt())

        if UserModel.find_by_username(username):
            return {"msg": "user with username exists"}
        
        user = UserModel(username,hashed)
        user.save_to_db()

        return {
            "msg": "user saved successfully"
        }


   





