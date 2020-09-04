from marsh import ma
from model.users import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id","activated")
        load_instance = True