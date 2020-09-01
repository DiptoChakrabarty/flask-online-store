from marsh import ma
from model.item import ItemModel
from model.stores import StoreModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True