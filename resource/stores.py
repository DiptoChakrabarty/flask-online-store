from flask_restful import Resource
from model.store import StoreModel
from flask import request
from schemas.stores import StoreSchema
from flask_jwt_extended import  jwt_required,fresh_jwt_required

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):
    def get(self):
        data=request.get_json()
        name=data["name"]

        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {"msg": "Store not found"},404
    
    @jwt_required
    def post(self):
        data=request.get_json()
        name=data["name"]

        store = StoreModel.find_by_name(name)
        if store:
            return {"msg": "Store exists already"},400
        
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"msg": "Error occured"},500

        return {"msg": "Added the store"},201
        
    @fresh_jwt_required    
    def delete(self):
        data=request.get_json()
        name=data["name"]

        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        else:
            return {"msg": "Store does not exist"},400
        return {"msg": "Store deleted"}



class StoreList(Resource):
    def get(self):
        return  {'stores': store_list_schema.dump(StoreModel.find_all())}


