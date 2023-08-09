from datetime import datetime

from mongoengine import EmbeddedDocument, Document, fields


class Lot(EmbeddedDocument):
    price = fields.IntField(required=True)
    quantity = fields.IntField(required=True)

    def __str__(self):
        return f"({self.price}, {self.quantity})"

    def __hash__(self):
        return hash(self.price * self.quantity)


class DateKey(Document):
    date = fields.DateTimeField(default=datetime.utcnow, unique=True)

    def __str__(self):
        return str(self.date)


class Item(Document):
    item_id = fields.IntField(required=True)
    date = fields.ReferenceField(DateKey)
    total_quantity = fields.IntField(required=True)
    average_price = fields.FloatField(required=True)
    auctions = fields.EmbeddedDocumentListField(Lot, default=list)

    def __str__(self):
        return str(self.item_id)
