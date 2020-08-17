
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This cannot be blank")

    parser.add_argument('name',
    required=True,
    help="This cannot be blank")

    def get(self):
        data = Item.parser.parse_args()
        #print(data)
        name = data["name"]
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {
            "msg": "Item not found"
        }
            
    
    def post(self):
        data = Item.parser.parse_args()
        name = data["name"]
        price = data["price"]
        print(data)

        item = ItemModel(name,price)

        try:
            item.save_to_db()
        except:
            return {"msg": "Error occured"}
        return item.json() , 201
    
    def delete(self):
        data = Item.parser.parse_args()
        name = data["name"]
        price = data["price"]

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"msg": "Item deleted successfully"}
        return {"msg": "Item not found"},404


    def put(self):
       
        data = Item.parser.parse_args()
        name = data["name"]
        price = data["price"]

        item = ItemModel.find_by_name(name)

        if item:
            item.price = price
        else:
            return item.json()
        
        item.save_to_db()

        return item.json()