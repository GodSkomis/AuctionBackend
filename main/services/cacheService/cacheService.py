from typing import List

from django.core.cache import caches
from django.core.cache import cache


class CacheService:

    @classmethod
    def get_item_auctions(cls, item_id: int) -> List | None:
        return cls.get_items_cache_object().get(item_id)

    @classmethod
    def set_item_auctions(cls, item_id: int, data: List, timeout: int = 60 * 60) -> bool:
        return cls.get_items_cache_object().add(item_id, data, timeout=timeout)

    @classmethod
    def clear_items(cls) -> bool:
        return cls.get_items_cache_object().clear()

    @staticmethod
    def get_items_cache_object() -> cache:
        return caches['items']
