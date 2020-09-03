from marsh import ma
from model.item import ItemModel
from model.store import StoreModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True