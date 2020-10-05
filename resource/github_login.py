from flask import g,jsonify,request,url_for
from flask_restful import Resource
from outh import github
from model.users import UserModel
from flask_jwt_extended import create_access_token,create_refresh_token
import secrets
import string

class Github(Resource):
    @classmethod
    def get(cls):
        return github.authorize(url_for("github.authorize",_external=True))

class GithubAuthorize(Resource):


    #generate a sample password for github oauth users
    @classmethod
    def generate_sample_password(cls):
        alpha = string.ascii_letters + string.digits
        random = ''.join(secrets.choice(alpha) for i in range(20))
        return random


    @classmethod
    def get(cls):
        response =  github.authorized_response()
        if response is None or response.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }
            return error_response


        g.access_token = response["access_token"]   #access token is made global
        github_user = github.get("user")  #user information object   
        github_username = github_user.data["login"]  #get github users username
        github_email = github_user.data["email"]
        
        #if UserModel.find_by_username(github_username):
        #    return {"msg": "User with username exists"}

        #add user to database
        user = UserModel(username=github_username,password=GithubAuthorize.generate_sample_password(),activated=True,email=github_email)
        user.save_to_db()

        #create jwt tokens
        access_token = create_access_token(identity=user.id,fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },200
        