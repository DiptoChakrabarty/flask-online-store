import os
from flask import Flask ,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CILENT_SECRET")
print(client_id,client_secret)

app= Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db=SQLAlchemy(app)
mograte = Migrate(app,db)



class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(20),nullable=False,unique=True)
    petname =  db.Column(db.String(20),nullable=False,server_default="true")

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/users",methods=["POST"])
def add_user():
    data=request.get_json()
    username=data["name"]
    email=data["email"]
    petname = data["petname"]
    
    user = Users(name=username,email=email,petname=petname)
    db.session.add(user)
    db.session.commit()

    return jsonify({ "msg": "Added User" , "status":200})

@app.route("/show",methods=["POST"])
def show_user():
    data=request.get_json()
    username=data["name"]
    
    user =  Users.query.filter_by(name=username).first()

    if user:
        return jsonify({
            "name": user.name,
            "email": user.email
        })
    
    return jsonify({
        "msg": "user does not exist"
    }),404





if __name__ =="__main__":
    app.run(debug=True)