from flask import g,jsonify
from flask_restful import Resource
from outh import github
from model.users import UserModel
from flask_jwt_extended import create_access_token,create_refresh_token

class Github(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback="http://localhost:5000/login/github/authorized")

class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        response =  github.authorized_response()
        g.access_token = response["access_token"]   #access token is made global
        github_user = github.get("user")  #user information object   
        github_username = github_user.data["login"]  #get github users username
        github_email = github_user.data["email"]
        
        #if UserModel.find_by_username(github_username):
        #    return {"msg": "User with username exists"}
        
        #add user to database
        user = UserModel(username=github_username,password=None,activated=True,email=github_email)
        user.save_to_db()

        #create jwt tokens
        access_token = create_access_token(identity=user.id,fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },200
        