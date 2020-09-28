from db import db
import stripe


CURRENCY="Rs"

class ItemsInOrder(db.Model):
    __tablename__="items_in_order"
    id= db.Column(db.Integer,primary_key=True)
    item_id=db.Column("item_id",db.Integer,db.ForeignKey("items.id"))
    order_id = db.Column("order_id",db.Integer,db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel",back_populates="items")


class OrderModel(db>Model):
    __tablename__="orders"

    id = db>Column(db.Integer,primary_key=True)
    status =  db.Column(db.String(15),nullable=True)

    items = db.relationship("ItemsInOrder",back_populates="items")


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

    def request_with_stripe(self,token: str)-> stripe.Charge:
        stripe.api_key =  os.getenv("API_KEY")

        return stripe.Charge.create(
            amount=self.amount,
            currency=CURRENCY,
            description=self.description,
            source=token
        )