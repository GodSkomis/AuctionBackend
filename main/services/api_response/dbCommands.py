from typing import TypedDict, List
import datetime

from .abstracts import AbstractDbCommand

from main.models.auction import DateKey, Item
from django.db.models import Q


class LotDict(TypedDict):
    price: int
    quantity: int


class ItemDict(TypedDict):
    lots: List[LotDict]
    date: datetime.datetime


class GetLotsCommand(AbstractDbCommand):
    _item_id: int

    def __init__(self, item_id: int):
        self._item_id = item_id

    def execute(self) -> List[ItemDict]:
        dates = DateKey.objects.all()
        items = Item.objects.values('lots', 'date').filter(Q(item_id=self._item_id) & Q(date__in=dates)).all()

        return items
