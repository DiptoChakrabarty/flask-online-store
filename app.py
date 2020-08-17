from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
import bcrypt

from security import auth,identity
from resource.users import users
from resource.items import Item

app = Flask(__name__)
app.secret_key="pinku"
api=Api(app)

jwt=JWT(app,auth,identity)

app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"


api.add_resource(Item,"/item")
api.add_resource(ItemList,"/items_show")
api.add_resource(users,"/register")

import routes

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True,host="0.0.0.0")