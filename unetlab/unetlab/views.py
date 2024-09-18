from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from unetlab import models


def index(request):
    # a = models.Config.objects.all()
    # print(a)
    return HttpResponse("Hello, world. You're at the polls index.")


#
# Lab
#


class LabList(ListView):
    model = models.Lab


class LabDetail(DetailView):
    model = models.Lab
