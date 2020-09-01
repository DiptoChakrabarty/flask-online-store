from db import db
import bcrypt
from typing import Dict,List,Union

UserJson = Dict[str,Union[int,str]]


class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False)

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self) -> UserJson:
        return {
            "id": self.id,
            "username": self.username
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
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
