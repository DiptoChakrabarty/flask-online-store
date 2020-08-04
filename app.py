from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT,jwt_required
import bcrypt
#from security import auth,identity

app = Flask(__name__)
api=Api(app)

app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"

db = SQLAlchemy(app)

#jwt = JWT(app,auth,identity )

class product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    price = db.Column(db.String(20),nullable=False)

class users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password

class users(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        passwd = data["password"]
        hashed = bcrypt.hashpw(passwd.encode('utf-8'),bcrypt.gensalt())

        new_user = users(username=username,password=hashed)
        db.session.add(new_user)
        db.sesssion.commit()
        return jsonify({
        "msg": "User Added",
        "status": 200
            })

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This cannot be blank")

    parser.add_argument('name',
    type=string,
    required=True,
    help="This cannot be blank")

    def get(self):
        data = Item.parser.parse_args()
        print(data)
        name = data["name"]
        item = product.query.filter_by(name=name).first()

        if item:
            ret = {
                "name": item.name,
                "price": item.price
            }
        else:
            ret = {
                "msg": "Not found"
            }
        return ret
    
    def post(self):
        data = Item.parser.parse_args()
        name = data["name"]
        price = data["price"]
        print(data)

        item = product(name=name,price=price)
        db.session.add(item)
        db.session.commit()
        ret = {
            "name": item.name,
            "price": item.price
        }
        return ret
    
    def delete(self):
        data = Item.parser.parse_args()
        name = data["name"]
        price = data["price"]

        item = product.query.filter_by(name=name)
        db.session.delete(item)
        db.session.commit()

        ret = {
            "msg": "Item Deleted"
        }
        return ret

    def put(self):
       
        data = Item.parser.parse_args()
        name = data["name"]
        price = data["price"]

        item = product.query.filter_by(name=name)
        item.price = price

        db.session.commit()

        ret = {
            "msg": "Item Updated with price {}".format(price)
        }
        return ret






class users(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        new_user = users(username=username,password=hashed )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "msg": "User Added",
            "status": 200
        })

@app.before_first_request
def create_tables():
    db.create_all()


#api.add_resource(Item,"/item/<string:name>")
api.add_resource(Item,"/item")
api.add_resource(users,"/user")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")