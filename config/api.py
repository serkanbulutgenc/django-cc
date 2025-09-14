from ninja import NinjaAPI

from apps.tariff.api import tariff_router

app = NinjaAPI(title="Tariff API", description="Custom tariff codes API")

app.add_router("tariff/", tariff_router)
