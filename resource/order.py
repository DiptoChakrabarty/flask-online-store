from flask_restful import Resource 
from flask import request
from model.item  import ItemModel
from model.order import OrderModel,ItemsInOrder
from collections import Counter


class Order(Resource):
    @classmethod
    def post(cls):
        data= request.get_json()
        items=[]
        item_quantity = Counter(data["items"])

        for name,count in item_quantity.most_commom():
            res = ItemModel.find_by_name(name)
            if not res:
                return {"msg": "Item not present {}".format(name)},404
            items.append(ItemsInOrder(name=name,quantity=count))
        #print(items)
    
        order = OrderModel(items=items,status="pending")
        order.save_to_db()


