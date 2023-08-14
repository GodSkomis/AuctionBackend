from abc import ABC, abstractmethod
from typing import Any

from django.http import HttpResponse


class AbstractDbCommand(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass


class AbstractDbResponseParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, db_response: Any) -> Any:
        pass


class AbstractApiResponseBuilder(ABC):
    _db_command: AbstractDbCommand
    _parser: AbstractDbResponseParser

    def __init__(self, db_command: AbstractDbCommand, parser: AbstractDbResponseParser):
        self._db_command = db_command
        self._parser = parser

    @abstractmethod
    def get_response(self) -> HttpResponse:
        pass
