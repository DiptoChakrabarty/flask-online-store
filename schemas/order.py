from marsh import ma
from model.order import OrderModel


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        load_only = ("token",)
        dump_only = ("id","status")
        include_fk = True