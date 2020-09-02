from marsh import ma
from model.users import UserModel

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    