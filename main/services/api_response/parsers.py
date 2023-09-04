from typing import List

from .abstracts import AbstractDbResponseParser
from main.models.auction import Item


class GetItemParser(AbstractDbResponseParser):

    @classmethod
    def parse(cls, items: List[Item]) -> List:
        return [{'date': str(items[i]['date']), 'lots': items[i]['lots']} for i in range(len(items))]
