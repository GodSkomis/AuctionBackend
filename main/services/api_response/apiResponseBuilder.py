from typing import Any

from django.http.response import JsonResponse

from .abstracts import AbstractApiResponseBuilder


class ApiResponseBuilder(AbstractApiResponseBuilder):
    def get_data(self) -> Any:
        db_response = self._db_command.execute()
        return self._parser.parse(db_response)

    @staticmethod
    def create_response(data: Any):
        return JsonResponse(data={"data": data}, status=200)
