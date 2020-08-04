


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
