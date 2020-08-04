from app import app,db,api
from resource.items import Item
from resource.users import users

@app.before_first_request
def create_tables():
    db.create_all()


#api.add_resource(Item,"/item/<string:name>")
api.add_resource(Item,"/item")
api.add_resource(users,"/user")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")