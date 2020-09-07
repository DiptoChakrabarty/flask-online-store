import os
from flask import Flask ,request,jsonify,url_for
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy 
from itsdangerous import URLSafeTimedSerializer,SignatureExpired

app= Flask(__name__)

serializer = URLSafeTimedSerializer("secrettoken")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db=SQLAlchemy(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] =  587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_DEFAULT_SENDER"] = ("Dipto from DLDLAB",os.environ["MAIL_USERNAME"])
app.config["MAIL_MAX_EMAILS"] = None
app.config["MAIL_SUPRESS_SEND"] = False
app.config["MAIL_ASCII_ATTACHMENTS"] =  False

mail = Mail(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(20),nullable=False)

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()



def tokens(email):
    serializer = URLSafeTimedSerializer("secrettoken",1800)
    token = serializer.dumps({"email": email},salt="flask-email-confirmation")
    return token




@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/send")
def send():
    msg =  Message("Hey There",recipients=["user@gmail.com"])
    msg.body = "This is a sample email for default users"
    #msg.html = "<br>Adding HTML to your email</br>"
    mail.send(msg)

    return f"Mail Sent Successfully"

@app.route("/register",methods=["POST"])
def register():
    data = request.get_json()
    name=data["name"]
    email = data["email"]
    print(name,email)

    user = Users(name=name,email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({ "msg": "Added User" , "status":200})

@app.route("/token",methods=["POST"])
def token_create():
    data = request.get_json()
    name=data["name"]
    email = data["email"]

    if Users.find_by_name(name):
        tok = tokens(email)
        print(tok)

        msg= Message("Confirm Email",recipients=[email])
        link = url_for("token_verify",token=tok,_external=True)
        msg.body = "Verify email address by clicking here {}".format(link)
        mail.send(msg)


        return jsonify({"msg": "your token is {}".format(tok)})
    return jsonify({"msg": "Invalid user"})

@app.route("/confirm/<token>")
def token_verify(token):
    try:
        serializer = URLSafeTimedSerializer("secrettoken")
        email = serializer.loads(token,salt="flask-email-confirmation")["email"]
        print(email)   
    except SignatureExpired:
        return "<h1>Token is expired</h1>"
    return "<h1>Token Verified</h1>"

if __name__ =="__main__":
    app.run(debug=True)