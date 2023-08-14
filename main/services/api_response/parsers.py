from typing import Dict, List

from .abstracts import AbstractDbResponseParser


class GetItemParser(AbstractDbResponseParser):

    @classmethod
    def parse(cls, db_response: (List, List)) -> List:
        return [{str(db_response[0][i].date): db_response[1][i]} for i in range(len(db_response[0]))]
