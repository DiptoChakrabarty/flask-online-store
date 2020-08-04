from flask import Flask,jsonify,request
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
api=Api(app)

app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"

db = SQLAlchemy(app)

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
    def get(self):
        data = request.get_json()
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
                "msg": Not found
            }
        return ret
    
    def post(self):
        data = request.get_json()
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

@app.before_first_request
def create_tables():
    db.create_all()


#api.add_resource(Item,"/item/<string:name>")
api.add_resource(Item,"/item")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")