from db import db
import bcrypt
from typing import Dict,List,Union
from flask import request,url_for
import requests
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from mail import mail 
from flask_mail import Message

MAILGUN_DOMAIN = "mailgun domain"
MAILGUN_API_KEY =  "api key"
FROM_TITLE = "Stores API"
FROM_EMAIL = "mailgun email"

UserJson = Dict[str,Union[int,str]]


class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=True)
    email = db.Column(db.String(40),nullable=False,unique=True)
    activated = db.Column(db.Boolean,default=False)    #set default as False , if you do not email verification set as True
    seller = db.Column(db.Boolean, default=False)

    def __init__(self,username,password,email,activated=False,seller=False): # if you do not email verification set activated as True
        self.username=username
        self.password=password
        self.email = email
        self.activated = activated
        self.seller = seller
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def generate_mail(self):
        serializer = URLSafeTimedSerializer("secrettoken",1800)
        token = serializer.dumps({"email":self.email},salt="flask-email-confirmation")
        
        msg= Message("Confirm Email",recipients=[self.email])
        #link = api.url_for(api(current_app),UserConfirm,token=tok,_external=True)
        link = "http://localhost:5000/confirm/{}".format(token)
        msg.body = "Verify email address by clicking here {}".format(link)
        mail.send(msg)

        
    


    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def check_password(cls,username,password):
        user=cls.query.filter_by(username=username).first()
        password = password.encode('utf-8')
        if user and bcrypt.checkpw(password,user.password):
            return True
        else:
            return False
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
