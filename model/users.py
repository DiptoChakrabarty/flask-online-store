from db import db
import bcrypt
from typing import Dict,List,Union
from flask import request,url_for
import requests
from libs import MailGun

MAILGUN_DOMAIN = "mailgun domain"
MAILGUN_API_KEY =  "api key"
FROM_TITLE = "Stores API"
FROM_EMAIL = "mailgun email"

UserJson = Dict[str,Union[int,str]]


class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),nullable=False,unique=True)
    activated = db.Column(db.Boolean,default=False)

    def __init__(self,username,password):
        self.username=username
        self.password=password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def send_mail(self):
        
        link = request.url_root[:-1] + url_for("userconfirm",user_id=self.username)
        subject= "Registration confirmation"
        text= f"Please click the link to confirm : {link}"
        html = f'<html>Please click the link to confirm : <a href="{link}">{link}</a></html>'

        MailGun.send_mail([self.email],subject,text,html)

        requests.post(
            f"http://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api",MAILGUN_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": self.email,
                "subject": "Registration confirmation",
                "text": f"Please click the link to confirm : {link}",
            },
        )


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
