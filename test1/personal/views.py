from django.shortcuts import render
from django.http import HttpResponse
import json

from .forms import TestForm
from personal.Speak import *
from personal.Core_Calcs import core_calcs


def index(request):
    if request.method == 'POST':
        data = [value for key, value in request.POST.dict().items()]
        data.pop(0)
        key_list = [data[0]] + [list(map(int, data[1:]))]
        test_list = core_calcs(key_list)
        print(test_list)
        results_list = [i[2] for i in test_list]
        print(results_list)
        ratios_pie = list(map(lambda x: x * 100, [i[1] for i in test_list]))
        ratios_pie = [round(i,2) for i in ratios_pie]
        print(ratios_pie)
        return render(request, "personal/home2.html", {"ratios_pie": ratios_pie, "results_list": results_list})
    return render(request, "personal/home.html")

def test1(request):
    return HttpResponse("hello world")
