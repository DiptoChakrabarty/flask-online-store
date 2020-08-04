from flask import Flask
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api=Api(app)

app.config["SECRET_KEY"]= "diptochuck"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    price = db.Column(db.String(20),nullable=False)



@app.before_first_request
def create_tables():
    db.create_all()





if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")