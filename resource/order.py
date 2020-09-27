from flask_restful import Resource 
from flask import request
from model.item  import ItemModel
from model.order import OrderModel


class Order(Resource):
    @classmethod
    def post(cls):
        data= request.get_json()
        items=[]

        for name in data["items"]:
            res = ItemModel.find_by_name(name)
            if not res:
                return {"msg": "Item not present {}".format(name)},404
            items.append(name)
        print(items)
    
        order = OrderModel(items=items,status="pending")
        order.save_to_db()
        

