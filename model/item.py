from db import db
from typing import Dict,List,Union

ItemJson =  Dict[str,Union[int,str,float]]




class ItemModel(db.Model):
    __tablename__="items"

    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(50),unique=True,nullable=False)
    price =  db.Column(db.Float(precision=2),nullable=False)

    store_id = db.Column(db.Integer,db.ForeignKey('stores.id'),nullable=False)
    store = db.relationship("StoreModel")

    
    @classmethod
    def find_by_name(cls,name: str):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()
    
    @classmethod
    def find_id(cls,name: str):
        obj = cls.query.filter_by(name=name).first()
        return obj.id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()