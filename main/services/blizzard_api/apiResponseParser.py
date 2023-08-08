from typing import List

from main.models import mongo


class ApiResponseParser:
    _api_auctions: dict
    _min_quantity = 1000

    def __init__(self, blizzard_api_response: dict):
        self._api_auctions = blizzard_api_response['auctions']

    def _parse_raw_response(self) -> None:
        result = {}
        for row in self._api_auctions:
            item_id = row['item']['id']
            count = row['quantity']
            price = row['unit_price']
            if price == 0:
                continue
            try:
                result[item_id].append((price, count))
            except KeyError:
                result[item_id] = [(price, count)]

        self._api_auctions = result

    def _get_items_list(self) -> List[mongo.Item]:
        result = []
        for item_id in (aucs := self._api_auctions):
            price_summ = 0
            quantity = 0
            lots = []
            raw_lots = aucs[item_id]
            raw_lots.sort()

            for i in range(len(raw_lots)):
                if quantity > 1000:
                    break

                lot_price = raw_lots[i][0]
                lot_quantity = raw_lots[i][1]

                quantity += lot_quantity
                price_summ += lot_price * lot_quantity

                lots.append(mongo.Lot(
                    price=lot_price,
                    quantity=lot_quantity
                ))

            item = mongo.Item()
            item.item_id = item_id
            item.auctions = lots
            item.total_quantity = quantity
            item.average_price = round(price_summ / quantity, 2)
            result.append(item)

        return result

    def parse(self) -> List[mongo.Item]:
        self._parse_raw_response()
        return self._get_items_list()
