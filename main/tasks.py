from auc.celery import app

from mongoengine.errors import NotUniqueError

from .services.blizzard_api import ApiService, ApiResponseParser
from .services.mongo import ConnectionClient

from .models.mongo import DateKey

import time
from pprint import pprint


# @app.task
# def update_names_task():
#     response = Updater._get_response()
#     j = response.json()
#     auctions,_ = Updater._parse_response(j)
#     item_ids = list(auctions.keys())
#     item_ids = get_names_for_update(item_ids)
#     item_ids.sort()
#     Updater._update_names(item_ids)
#     return str(datetime.datetime.now())

@app.task
def update_items_task() -> str:
    start_time = time.time()
    service = ApiService()
    time_of_update, api_response = service.get_auction_response()
    with ConnectionClient():
        try:
            check_time = DateKey.objects.filter(date=time_of_update)
            if check_time:
                raise ValueError(f"REPEATED DATA {check_time}")
        except NotUniqueError:
            return 0

    api_response_parser = ApiResponseParser(api_response)

    dateKey = DateKey()
    dateKey.date = time_of_update
    items = api_response_parser.parse()
    with ConnectionClient() as c:
        dateKey.save()
        for i in items:
            i.date = dateKey
            i.save()

    finish_time = time.time()
    result = F"TIME OF UPDATE: {finish_time - start_time}"
    pprint(result)
    return result


app.conf.beat_schedule = {
    "update_items_task": {
        "task": "main.tasks.update_items_task",
        "schedule": 211.0
    }
}
