from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.core.serializers import serialize
from datetime import datetime
from damlevelsapp.models import DamLevels
from django.template.context import Context
import pandas as pd


# Create your views here.
def dam_dataset(request):
    damlevels = serialize('geojson', DamLevels.objects.all())
    return HttpResponse(damlevels, content_type='json')

def home(request):
    """Renders Home Page"""
    return render(
        request, 'app/index.html'
    )

