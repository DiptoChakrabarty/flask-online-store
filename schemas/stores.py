from marsh import ma
from model.stores import StoreModel
from model.item import ItemModel
from schemas.items import ItemSchema


class StoreSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema,many=True)
    class Meta:
        model = StoreModel
        dump_only = ("id",)
        include_fk = True