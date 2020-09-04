from flask_restful import Resource,reqparse
import bcrypt
from model.users import UserModel
from flask import request
from flask_jwt_extended import ( create_access_token,
create_refresh_token,jwt_refresh_token_required,get_jwt_identity,jwt_required)
from blacklist import black
from schemas.users import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()

class userregister(Resource):
    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,400
        username = data.username
        passwd = data.password
        print(username,passwd)
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
        
        return user_schema.dump(user),200
    
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "User not found"},404
        user.delete_from_db()
        
        return {"msg": "user deleted successfully"}

class userlogin(Resource):
    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,400
        username = data.username
        password = data.password

        user = UserModel.find_by_username(username)

        if user and UserModel.check_password(username,password):
            if user.activated:
                access_token = create_access_token(identity=user.id,fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },200
            return {"msg": "User has not yet been activated"},401
        
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
   
class UserConfirm(Resource):
    def get(self):
        data = request.get_json*()
        user_find = user_schema.load(data)

        if user_find.find_by_username(user_find.username):
            user_find.activated = True
            user_find.save_to_db()
            return {"msg": "User has been activated"},200
        return {"msg": "User not found"},404




