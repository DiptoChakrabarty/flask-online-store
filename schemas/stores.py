from marsh import ma
from model.store import StoreModel
from model.item import ItemModel
from schemas.items import ItemSchema


class StoreSchema(ma.Schema):
    items = ma.Nested(ItemSchema,many=True)
    class Meta:
        model = StoreModel
        dump_only = ("id",)
        include_fk = True