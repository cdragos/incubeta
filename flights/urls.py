from django.urls import path

from .views import flight_search_view

urlpatterns = [
    path("flight-search/", flight_search_view, name="flight_search"),
]
