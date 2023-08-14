from django.urls import path
from .views import *

urlpatterns = [
    path("item/<int:item_id>", GetItemView.as_view(), name="get_item")
]
