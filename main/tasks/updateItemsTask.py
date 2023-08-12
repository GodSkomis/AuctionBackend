import datetime
import time
from typing import List
from celery import Task
from celery.signals import worker_ready

from pprint import pprint
from mongoengine.errors import NotUniqueError

from auc.celery import app

from main.services.blizzard_api import ApiService, ApiResponseParser
from main.services.mongo import ConnectionClient
from main.models.mongo import DateKey, Item


class UpdateItemsTask(Task):

    def run(self, *args, **kwargs):
        start_time = time.time()
        datetime_of_update, api_response = self._get_api_response()
        dateKey = self._check_time(datetime_of_update)
        if dateKey:
            self._handle_dateKey(dateKey)
            return self._print_final_time(start_time)

        self._handle_without_datyKey(datetime_of_update, api_response)
        return self._print_final_time(start_time)

    @staticmethod
    def _get_api_response() -> (datetime.datetime, dict):
        service = ApiService()
        return service.get_auction_response()

    @staticmethod
    def _check_time(datetime_of_update: datetime.datetime) -> None | DateKey:
        dateKey = None
        with ConnectionClient():
            dateKey = DateKey.objects.filter(date=datetime_of_update).first()
            if dateKey:
                dateKey = dateKey.select_related()
        return dateKey

    def _handle_dateKey(self, dateKey: DateKey) -> None:
        new_eta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        pprint(f"NEXT TIME OF UPDATE {new_eta}")
        pprint(f"REPEATED DATA {dateKey}")

        self.apply_async(eta=new_eta)

    def _handle_without_datyKey(self, datetime_of_update: datetime.datetime, api_response: dict) -> None:
        items = self._parse_response(api_response)
        dateKey = self._create_dateKey(datetime_of_update)
        self._set_date_for_items(dateKey, items)
        self._save_objects(dateKey, items)

        new_eta = datetime_of_update + datetime.timedelta(hours=1, minutes=1)
        self.apply_async(eta=new_eta)

        pprint(f"Next time of update {new_eta}")

    @staticmethod
    def _parse_response(api_response: dict) -> List[Item]:
        api_response_parser = ApiResponseParser(api_response)
        return api_response_parser.parse()

    @staticmethod
    def _create_dateKey(datetime_of_update: datetime.datetime) -> DateKey:
        dateKey = DateKey()
        dateKey.date = datetime_of_update
        return dateKey

    @staticmethod
    def _set_date_for_items(dateKey: DateKey, items: List[Item]) -> None:
        for item in items:
            item.date = dateKey

    @staticmethod
    def _save_objects(dateKey: DateKey, items: List[Item]) -> None:
        with ConnectionClient():
            dateKey.save()
            for item in items:
                item.save()

    @staticmethod
    def _print_final_time(start_time: float) -> float:
        final_time = round(time.time() - start_time, 2)
        print(final_time)
        return final_time


app.register_task(UpdateItemsTask())


@worker_ready.connect
def at_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task("main.tasks.updateItemsTask.UpdateItemsTask", connection=conn)
