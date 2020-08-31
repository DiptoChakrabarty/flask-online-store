from db import db
from typing import Dict,List,Union

ItemJson =  Dict[str,Union[int,str,float]]


class ItemModel(db.Model):
    __tablename__="items"

    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(50),unique=True)
    price =  db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer,db.ForeignKey('stores.id'))
    store = db.relationship("StoreModel")

    def __init__(self,name: str,price: float,store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self) -> ItemJson:
        return {
            "id": self.id,
        'name': self.name,
        'price': self.price,
        "store_id": self.store_id
        }

    @classmethod
    def find_by_name(cls,name: str):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()