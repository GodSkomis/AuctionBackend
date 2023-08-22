from typing import List

from django.http import HttpResponse

from main.services.cacheService import CacheService

from .apiResponseBuilder import ApiResponseBuilder
from .dbCommands import GetDbLotsCommand
from .parsers import GetItemParser


class ApiResponseDirector:

    @classmethod
    def get_item_response(cls, item_id: int) -> HttpResponse:
        data = cls._get_from_cache(item_id)
        if not data:
            data = cls._get_data_from_db(item_id)

        cls._set_to_cache(item_id, data)
        return cls._create_response(data)

    @staticmethod
    def _get_from_cache(item_id: int) -> None | List:
        return CacheService.get_item_auctions(item_id)

    @staticmethod
    def _get_data_from_db(item_id: int) -> HttpResponse:
        db_command = GetDbLotsCommand(item_id)
        parser = GetItemParser()
        builder = ApiResponseBuilder(db_command=db_command, parser=parser)
        return builder.get_data()

    @staticmethod
    def _create_response(data: List) -> HttpResponse:
        return ApiResponseBuilder.create_response(data)

    @staticmethod
    def _set_to_cache(item_id: int, data: List) -> bool:
        return CacheService.set_item_auctions(item_id, data)
