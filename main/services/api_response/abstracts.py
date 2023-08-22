from abc import ABC, abstractmethod
from typing import Any

from django.http import HttpResponse


class AbstractCommand(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass


class AbstractItemCommand(AbstractCommand, ABC):
    _item_id: int

    def __init__(self, item_id: int):
        self._item_id = item_id


class AbstractDbResponseParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, db_response: Any) -> Any:
        pass


class AbstractApiResponseBuilder(ABC):
    _db_command: AbstractCommand
    _parser: AbstractDbResponseParser

    def __init__(self, db_command: AbstractCommand, parser: AbstractDbResponseParser):
        self._db_command = db_command
        self._parser = parser

    @abstractmethod
    def get_data(self) -> HttpResponse:
        pass
