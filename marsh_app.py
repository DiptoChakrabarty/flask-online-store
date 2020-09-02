from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

app =Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db=SQLAlchemy(app)
ma = Marshmallow(app)


class Marsh(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))
    rewards = db.relationship("Reward")

class Reward(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    reward_name = db.Column(db.String(10))
    marsh_id = db.Column(db.Integer,db.ForeignKey("marsh.id"))
    marsh = db.relationship("Marsh",backref='reward')

class MarshSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Marsh
        load_instance = True
        

class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward
        load_instance = True
        



@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def home():
    one = Marsh(name="one")
    two = Marsh(name="two")
    db.session.add(one)
    db.session.add(two)
    db.session.commit()
    first = Reward(reward_name="reward1",marsh=one)
    second = Reward(reward_name="reward2",marsh=one)
    third = Reward(reward_name="reward3",marsh=two)
    db.session.add(first)
    db.session.add(second)
    db.session.add(second)
    db.session.commit ()
    users = Marsh.query.first() 
    print(users)
    rewards = Reward.query.all()
    print(rewards)
    return jsonify({"msg": "added to database"})

@app.route("/check")
def index():
    users = Marsh.query.first()
    print(users)
    marsh_schema =  MarshSchema()
    output = marsh_schema.dump(users)
    print(output)
    return jsonify({"user": output})

@app.route("/res")
def rewards():
    rewards = Reward.query.first()
    print(rewards)
    schema =  RewardSchema()
    output = schema.dump(rewards)
    print(output)
    return jsonify({"user": output})

@app.route("/checkall")
def index_all():
    users = Marsh.query.all()
    print(users)
    marsh_schema =  MarshSchema(many=True)
    output = marsh_schema.dump(users)
    print(output)
    return jsonify({"user": output})


if __name__=="__main__":
    app.run(debug=True)

