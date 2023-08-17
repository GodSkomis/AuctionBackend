from django.db import models


class DateKey(models.Model):
    date = models.DateTimeField(primary_key=True)

    def __str__(self):
        return str(self.date)


class Item(models.Model):
    item_id = models.IntegerField(blank=False)
    date = models.ForeignKey(DateKey, on_delete=models.CASCADE)
    lots = models.JSONField(default=list)

    def __str__(self):
        return str(self.item_id)
