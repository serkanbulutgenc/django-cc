from ninja import Router
from ninja import Schema

from apps.tariff.models import Tariff


class TariffSchema(Schema):
    id: int = None
    position_number: str | None = None
    item_definition: str | None = None
    item_type: str | None = None
    children: "list[TariffSchema]" = None


TariffSchema.model_rebuild()  # !!! this is important

tariff_router = Router()


@tariff_router.get("/", response=list[TariffSchema])
def tariff_list(request) -> list[TariffSchema]:
    return Tariff.objects.filter(level=0)
