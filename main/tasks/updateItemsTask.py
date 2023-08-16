import datetime
import time
from typing import List
from celery import Task
from celery.signals import worker_ready

from pprint import pprint

from auc.celery import app

from main.services.blizzard_api import ApiService, ApiResponseParser
from main.models.auction import DateKey, Item, Lot


class UpdateItemsTask(Task):

    def run(self, *args, **kwargs):
        was_updated = kwargs.get('was_updated', False)
        start_time = time.time()
        datetime_of_update, api_response = self._get_api_response()
        if self._check_time(datetime_of_update):
            self._repeat(datetime_of_update, was_updated)
            return self._print_final_time(start_time)

        self._handle_without_dateKey(datetime_of_update, api_response)
        return self._print_final_time(start_time)

    @staticmethod
    def _get_api_response() -> (datetime.datetime, dict):
        service = ApiService()
        return service.get_auction_response()

    @staticmethod
    def _check_time(datetime_of_update: datetime.datetime) -> None | DateKey:
        return DateKey.objects.filter(date=datetime_of_update).exists()

    def _repeat(self, time_of_update: datetime.datetime, was_updated: bool) -> None:
        pprint(f"REPEATED DATA {time_of_update}")
        if was_updated is False:
            new_eta = datetime.datetime.utcnow().replace(microsecond=0) + datetime.timedelta(minutes=10)
            pprint(f"NEXT TIME OF UPDATE {new_eta}")
            self.apply_async(kwargs={'was_updated': True}, eta=new_eta)

    def _handle_without_dateKey(self, datetime_of_update: datetime.datetime, api_response: dict) -> None:
        dateKey = self._create_dateKey(datetime_of_update)
        new_eta = datetime_of_update.replace(microsecond=0) + datetime.timedelta(hours=1, minutes=10)
        self._save_dateKey(dateKey)
        items, lots = self._parse_response(api_response)
        self._set_date_for_items(dateKey, items)
        self._save_items(items)
        self._save_lots(lots)

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
    def _save_dateKey(dateKey: DateKey) -> None:
        dateKey.save()

    @staticmethod
    def _set_date_for_items(dateKey: DateKey, items: List[Item]) -> None:
        for item in items:
            item.date = dateKey

    @staticmethod
    def _save_items(items: List[Item]) -> None:
        for item in items:
            item.save()

    @staticmethod
    def _save_lots(lots: List[List[Lot]]) -> None:
        for query in lots:
            for lot in query:
                lot.save()

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
