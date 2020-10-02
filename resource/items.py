
from flask_restful import Resource
from flask import request
from flask_jwt_extended import ( jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required)
from model.item import ItemModel
from marshmallow import ValidationError
from schemas.items import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Item(Resource):
    
    def get(self):
        try:
            data = item_schema.load(request.get_json())
            print(data.name)
        except ValidationError as err:
            return err.messages,400
        print(data)
        name = data.name
        item = ItemModel.find_by_name(name)

        if item:
            return item_schema.dump(item)
        return {
            "msg": "Item not found"
        }
            
    @jwt_required
    def post(self):
        try:
            item = item_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,400
        name = item.name
        price = item.price
        store_id = item.store_id
        #print(data)

        try:
            item.save_to_db()
        except:
            return {"msg": "Error occured"}
        return item_schema.dump(item) , 201
    
    @fresh_jwt_required
    def delete(self):
        try:
            item = item_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,400
        name = item.name
        item_check = ItemModel.find_by_name(name)
        if item_check:
            item_check.delete_from_db()
            return {"msg": "Item deleted successfully"}
        return {"msg": "Item not found"},404


    @jwt_required
    def put(self):
        data=request.get_json()
        name=data["name"]
        price = data["price"]

        item = ItemModel.find_by_name(name)

        if item:
            item.price = price
        else:
            return item.json()
        
        item.save_to_db()

        return item_schema.dump(item),  200

class ItemList(Resource):
    def get(self):
        return {'items': item_list_schema.dump(ItemModel.find_all()) },200