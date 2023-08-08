from datetime import datetime

from mongoengine import EmbeddedDocument, Document, fields


class Lot(EmbeddedDocument):
    price = fields.IntField(required=True)
    quantity = fields.IntField(required=True)

    def __str__(self):
        return f"({self.price}, {self.quantity})"


class Item(EmbeddedDocument):
    item_id = fields.IntField(required=True, unique=True)
    total_quantity = fields.IntField(required=True)
    average_price = fields.FloatField(required=True)
    auctions = fields.EmbeddedDocumentListField(Lot, default=list)

    def __str__(self):
        return str(self.item_id)


class DateKey(Document):
    date = fields.DateTimeField(default=datetime.now, unique=True)
    items = fields.EmbeddedDocumentListField(Item, default=list)

    def __str__(self):
        return str(self.date)
