from django.urls import path

from apps.tariff.views import list_view

app_name = "tariff"
urlpatterns = [path("", list_view, name="list")]
