from flask_restful import Resource 
from flask import request
from model.item  import ItemModel
from model.order import OrderModel,ItemsInOrder
from schemas.order import OrderSchema
from collections import Counter


order_schema=OrderSchema()



class Order(Resource):
    @classmethod
    def post(cls):
        data= request.get_json()
        items=[]
        ordered_list = data['items'] # list of dictionaries

        for ordered_item in data['items']:
            name = ordered_item['name']
            count = ordered_item['qty']
            res = ItemModel.find_by_name(name)
            if not res:
                return {"msg": "Item not present {}".format(name)},404
            items.append(ItemsInOrder(item_id=ItemModel.find_id(name),quantity=count))
        print(items)

        order = OrderModel(items=items,status="pending")
        order.save_to_db()  #save orders to database

        order.change_status("failed")
        order.request_with_stripe() #send the order details to stripe
        print("Payment Done")
        order.change_status("success")

        return order_schema.dump(order)


