from db import db
from dotenv import load_dotenv
load_dotenv() 
from stripe_pay import stripe


CURRENCY="INR"

class ItemsInOrder(db.Model):
    __tablename__="items_in_order"
    id= db.Column(db.Integer,primary_key=True)
    item_id=db.Column("item_id",db.Integer,db.ForeignKey("items.id"))
    order_id = db.Column("order_id",db.Integer,db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel",back_populates="items")


class OrderModel(db.Model):
    __tablename__="orders"

    id = db.Column(db.Integer,primary_key=True)
    status =  db.Column(db.String(15),nullable=True)

    items = db.relationship("ItemsInOrder",back_populates="order")


    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
    
    @property
    def description(self):
        counts= [f'{data.quantity}x {data.item.name}' for data in self.items]
        return ",".join(counts)
    
    @property
    def amount(self):
        total = int(sum([item_data.item.price*item_data.quantity for item_data in self.items])*100)
        return total

    def change_status(self,new_status):
        self.status = new_status
        self.save_to_db()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def request_with_stripe(self)-> stripe.Charge:
        token=stripe.Token.create(
        card={
            "number": "4242424242424242",
            "exp_month": 9,
            "exp_year": 2021,
            "cvc": "314",
            }, )
        
        print("The token id is ",token["id"])
        print("The amount is ",self.amount)

        return stripe.Charge.create(
            amount=self.amount,
            currency=CURRENCY,
            description=self.description,
            source=token["id"],
            shipping={
                'name': "John",
                'address': {
                'line1': '510 Townsend St',
                'postal_code': '98140',
                'city': 'Kolkata',
                'state': 'WB',
                'country': 'India',
            }
        })