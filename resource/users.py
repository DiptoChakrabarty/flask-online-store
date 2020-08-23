from flask_restful import Resource,reqparse
import bcrypt
from model.users import UserModel
from flask import request
from flask_jwt_extended import ( create_access_token,
create_refresh_token,jwt_refresh_token_required,get_jwt_identity)
from blacklist import black

class userregister(Resource):
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

class usermethods(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "User not found"},404
        
        return user.json
    
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "User not found"},404
        user.delete_from_db()
        
        return {"msg": "user deleted successfully"}

class userlogin(Resource):
    def post(self):
        data=request.get_json()
        username = data["username"]
        password = data["password"]

        user = UserModel.find_by_username(username)

        if user and UserModel.check_password(username,password):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            },200
        
        return {"msg": "wrong creds"},401
    
class logoutuser(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        black.add(jti)

        return {
            "msg": "Successfully logged out user"
        }

class tokenrefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {
            "access_token": new_token
        }
   





