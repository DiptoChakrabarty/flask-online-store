from flask_restful import Resource,reqparse,current_app
import bcrypt
from model.users import UserModel
from flask import request,make_response,render_template,jsonify
from flask_jwt_extended import ( create_access_token,
create_refresh_token,jwt_refresh_token_required,get_jwt_identity,jwt_required,get_raw_jwt)
from blacklist import black
from schemas.users import UserSchema
from marshmallow import ValidationError
from mail import mail 
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired

user_schema = UserSchema()

class UserRegister(Resource):
    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,400
        username = data.username
        passwd = data.password
        email = data.email
        seller = data.seller

        print(username,passwd,email)
        hashed = bcrypt.hashpw(passwd.encode('utf-8'),bcrypt.gensalt())

        if UserModel.find_by_username(username):
            return {"msg": "user with username exists"}
        
        if UserModel.find_by_email(email):
            return {"msg": "user with email id  exists"} 
        
        user = UserModel(username,hashed,email,seller=seller)
        user.save_to_db()

        user.generate_mail()     #send emails to new users

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
        email = data.email
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
    def get(self,token):
        try:
            serializer = URLSafeTimedSerializer("secrettoken")
            email = serializer.loads(token,salt="flask-email-confirmation")["email"]
            user = UserModel.find_by_email(email)
            if not user:
                return "<h1>Invalid User</h1>"
            user.activated = True 
            user.save_to_db()

        except:
            return "<h1>Token is expired</h1>"
        return "<h1>Token Verified</h1>"
    


        




