from typing import List

from main.models import auction


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

    def _get_items_list(self) -> (List[auction.Item], List[List[auction.Lot]]):
        items_result = []
        lots_result = []
        for item_id in (aucs := self._api_auctions):
            price_summ = 0
            quantity = 0
            hash_lots = {}
            raw_lots = aucs[item_id]
            raw_lots.sort()

            item = auction.Item()
            item.item_id = item_id

            for i in range(len(raw_lots)):
                if quantity > 1000:
                    break

                lot_price = raw_lots[i][0]
                lot_quantity = raw_lots[i][1]

                quantity += lot_quantity
                price_summ += lot_price * lot_quantity

                if lot_price not in hash_lots:
                    hash_lots[lot_price] = auction.Lot(
                        item_entry=item,
                        price=lot_price,
                        quantity=lot_quantity
                    )
                else:
                    lot = hash_lots[lot_price]
                    lot.quantity += lot_quantity

            lots_result.append(list(hash_lots.values()))
            item.total_quantity = quantity
            items_result.append(item)

        return items_result, lots_result

    def parse(self) -> (List[auction.Item], List[List[auction.Lot]]):
        self._parse_raw_response()
        return self._get_items_list()
