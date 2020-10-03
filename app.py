from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads,patch_request_class
import bcrypt,os
from mail import mail 
from dotenv import load_dotenv
load_dotenv()


from security import auth,identity
from resource.users import UserRegister,usermethods,userlogin,tokenrefresh,logoutuser,UserConfirm
from resource.items import Item,ItemList
from resource.stores import  Store,StoreList
from  resource.image import ImageUpload,Images
from libs.image_uploader import image_set
from blacklist import black
from outh import oauth
from resource.github_login import Github,GithubAuthorize
from resource.order import Order

#from marshmallow import ValidationError

from marsh import ma

app = Flask(__name__)
app.secret_key="pinku"
api=Api()

app.config["UPLOADED_IMAGES_DEST"] = os.path.join("static","images")


app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["PROPAGATE_EXCEPTIONS"]= True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"]=["access","refresh"]


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] =  587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")    #uncomment lines
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = ("Dipto from DLDLAB",os.environ["MAIL_USERNAME"])
app.config["MAIL_MAX_EMAILS"] = None
app.config["MAIL_SUPRESS_SEND"] = False
app.config["MAIL_ASCII_ATTACHMENTS"] =  False

patch_request_class(app,20*1024*1024)
configure_uploads(app,image_set)

@app.before_first_request
def create_tables():
    db.create_all()
    
jwt=JWTManager(app)


'''@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages),400'''



@jwt.user_claims_loader
def add_claims(identity):
    if identity == 1:
        return {
            "is_admin": True
        }
    return {
        "is_admin": False
    }

@jwt.token_in_blacklist_loader
def check_if_token_blacklist(decrypted_token):
    return decrypted_token["jti"] in black

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "The token has expired",
        "error": "token_expired"
    }),401

@jwt.invalid_token_loader
def invalid_token_Callback(error):
    return jsonify({
        "description": "Signature Invalid",
        "error": "invalid_token"
    }),401

@jwt.unauthorized_loader
def unaouthorized_token(error):
    return jsonify({
        "description": "jwt token not found",
        "error": "token_missing"
    }),401

@jwt.needs_fresh_token_loader
def fresh_token_loader():
    return jsonify({
        "description": "Require fresh token",
        "error": "fresh_token_required"
    }),401

@jwt.revoked_token_loader
def revoked_token():
    return jsonify({
        "description": "Token has been revoked",
        "error": "token_revoked"
    }),401



api.add_resource(Item,"/item")
api.add_resource(ItemList,"/itemsall")
api.add_resource(UserRegister,"/register")
api.add_resource(Store,"/store")
api.add_resource(StoreList,"/storesall")
api.add_resource(usermethods,"/user/<int:user_id>")
api.add_resource(userlogin,"/auth")
api.add_resource(tokenrefresh,"/refresh")
api.add_resource(logoutuser,"/logout")
#api.add_resource(UserConfirm,"/confirm")
api.add_resource(UserConfirm,"/confirm/<string:token>")    #confirm user method
api.add_resource(ImageUpload,"/imageupload") 
api.add_resource(Images,"/image")
api.add_resource(Github,"/login/github")
api.add_resource(GithubAuthorize,"/login/github/authorized",endpoint="github.authorize")
api.add_resource(Order,"/order")

if __name__ == "__main__":
    from db import db
    api.init_app(app)
    ma.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)
    app.run(debug=True,host="0.0.0.0")