from mongoengine import IntField, Document, StringField, URLField


class ProductInfo(Document):
    product_id = IntField()
    name = StringField()
    thumbnail = URLField()
    picture = URLField()
    description = StringField()
    supplier = StringField()
    meta = {
        'indexes': ['product_id', 'supplier'],
    }
