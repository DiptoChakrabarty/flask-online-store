from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_jwt_extended import JWTManager
import bcrypt

from security import auth,identity
from resource.users import userregister,usermethods,userlogin,tokenrefresh
from resource.items import Item,ItemList
from resource.stores import  Store,StoreList

app = Flask(__name__)
app.secret_key="pinku"
api=Api(app)



app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["PROPAGATE_EXCEPTIONS"]= True

@app.before_first_request
def create_tables():
    db.create_all()
    
jwt=JWTManager(app)

@jwt.user_claims_loader
def add_claims(identity):
    if identity == 1:
        return {
            "is_admin": True
        }
    return {
        "is_admin": False
    }

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
def unaouthorized_token():
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


api.add_resource(Item,"/item")
api.add_resource(ItemList,"/items_show")
api.add_resource(userregister,"/register")
api.add_resource(Store,"/store")
api.add_resource(StoreList,"/storesall")
api.add_resource(usermethods,"/user/<int:user_id>")
api.add_resource(userlogin,"/auth")
api.add_resource(tokenrefresh,"/refresh")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True,host="0.0.0.0")