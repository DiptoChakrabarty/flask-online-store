from db import db
from model.item import ItemJson




class StoreModel(db.Model):
    __tablename__="stores"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False,unique=True)
    
    items =  db.relationship("ItemModel",lazy="dynamic")


    @classmethod
    def find_by_name(cls,name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()