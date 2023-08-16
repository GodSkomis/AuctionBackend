from typing import NewType, List

from .abstracts import AbstractDbCommand

from main.models.auction import DateKey, Item, Lot
from django.db.models import Q


Lots = NewType('Items', List[dict])


class GetLotsCommand(AbstractDbCommand):
    _item_id: int

    def __init__(self, item_id: int):
        self._item_id = item_id

    def execute(self) -> (List[DateKey], List[Lots]):
        dates = list(DateKey.objects.all())
        items = Item.objects.filter(Q(item_id=self._item_id) & Q(date__in=dates)).all()
        lots = list(Lot.objects.values('price', 'quantity').filter(item_entry__in=items).all())

        return dates, lots
