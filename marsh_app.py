from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

app =Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db=SQLAlchemy(app)
ma = Marshmallow(app)


class marsh(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))

class reward(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    reward_name = db.Column(db.String(10))
    user_id = db.Column(db.Integer,db.ForeignKey("marsh.id"))
    marsh = db.relationship("marsh",backref='rewards')

class MarshSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = marsh
        load_instance = True
        include_fk = True

class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = reward
        load_instance = True



@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def home():
    one = marsh(name="one")
    two = marsh(name="two")
    db.session.add(one)
    db.session.add(two)
    db.session.commit()
    first = reward(reward_name="reward1",marsh=one)
    second = reward(reward_name="reward2",marsh=one)
    third = reward(reward_name="reward3",marsh=two)
    db.session.add(first)
    db.session.add(second)
    db.session.add(second)
    db.session.commit 
    users = marsh.query.first() 
    print(users)
    return jsonify({"msg": "added to database"})

@app.route("/check")
def index():
    users = marsh.query.first()
    print(users)
    marsh_schema =  MarshSchema()
    output = marsh_schema.dump(users)
    print(output)
    return jsonify({"user": output})


if __name__=="__main__":
    app.run(debug=True)

