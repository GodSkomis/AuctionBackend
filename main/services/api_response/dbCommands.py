from typing import NewType, List, Dict

from .abstracts import AbstractDbCommand

from main.services.mongo import ConnectionClient
from main.models.mongo import DateKey, Item

Dates = NewType('Dates', List[DateKey])
Items = NewType('Items', List[Dict])


class GetItemDbCommand(AbstractDbCommand):
    _item_id: int

    def __init__(self, item_id: int):
        self._item_id = item_id

    def execute(self) -> (Dates, Items):
        with ConnectionClient():
            dates = DateKey.objects.all().select_related()
            items = Item.objects.exclude('id').exclude('date').filter(item_id=self._item_id).as_pymongo().select_related()

        return dates, items
