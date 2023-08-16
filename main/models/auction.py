from django.db import models


class DateKey(models.Model):
    date = models.DateTimeField(primary_key=True)

    def __str__(self):
        return str(self.date)


class Item(models.Model):
    item_id = models.IntegerField(blank=False)
    date = models.ForeignKey(DateKey, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.item_id)


class Lot(models.Model):
    item_entry = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.BigIntegerField(blank=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return f"({self.price}, {self.quantity})"
