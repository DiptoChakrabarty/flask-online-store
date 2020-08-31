from marshmallow import Schema,fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)