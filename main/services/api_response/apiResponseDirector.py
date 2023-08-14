from django.http import HttpResponse
from .apiResponseBuilder import ApiResponseBuilder
from .dbCommands import GetItemDbCommand
from .parsers import GetItemParser


class ApiResponseDirector:

    @classmethod
    def get_item_response(cls, item_id: int) -> HttpResponse:
        db_command = GetItemDbCommand(item_id)
        parser = GetItemParser()
        builder = ApiResponseBuilder(db_command=db_command, parser=parser)
        return builder.get_response()
