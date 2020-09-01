from marsh import ma
from model.users import UserModel

class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
    