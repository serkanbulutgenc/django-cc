from django.shortcuts import render

from apps.tariff.models import Tariff

# Create your views here.


def list_view(request):
    return render(
        request=request,
        template_name="tariff/list.html",
        context={"tariffs": Tariff.objects.all()},
    )
