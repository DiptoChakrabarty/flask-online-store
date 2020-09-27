from db import db

class OrderModel(db>Model):
    __tablename__="orders"

    id = db>Column(db.Integer,primary_key=True)
    status =  db.Column(db.String(15),nullable=True)

    items = db.relationship("ItemModel",lazy="dynamic")


    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def change_status(self,new_status):
        self.status = new_status
        self.save_to_db()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def save_to_db(self):
        db.session.delete(self)
        db.session.commit()