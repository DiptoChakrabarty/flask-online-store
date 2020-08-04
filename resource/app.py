from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT,jwt_required
import bcrypt
#from security import auth,identity
from flask_sqlalchemy import SQLAlchemy

app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"

db = SQLAlchemy(app)

app = Flask(__name__)
api=Api(app)


from online import routes

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")