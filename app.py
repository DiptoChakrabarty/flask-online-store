from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_jwt_extended import JWTManager
import bcrypt

from security import auth,identity
from resource.users import userregister,usermethods,userlogin
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

api.add_resource(Item,"/item")
api.add_resource(ItemList,"/items_show")
api.add_resource(userregister,"/register")
api.add_resource(Store,"/store")
api.add_resource(StoreList,"/storesall")
api.add_resource(usermethods,"/user/<int:user_id>")
api.add_resource(userlogin,"/auth")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True,host="0.0.0.0")