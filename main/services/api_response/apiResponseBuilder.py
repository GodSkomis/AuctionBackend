from django.http import HttpResponse
from django.http.response import JsonResponse

from .abstracts import AbstractApiResponseBuilder


class ApiResponseBuilder(AbstractApiResponseBuilder):

    def get_response(self) -> HttpResponse:
        db_response = self._db_command.execute()
        data = self._parser.parse(db_response)
        return JsonResponse(data={"data": data}, status=200)
