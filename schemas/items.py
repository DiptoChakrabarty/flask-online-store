from marsh import ma
from model.item import ItemModel
from model.store import StoreModel


class ItemSchema(ma.Schema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True