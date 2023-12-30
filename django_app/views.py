import json
import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.cache import caches
from django_app import models
from django_settings import utils

RamCache = caches["default"]


def home(request):
    if request.method == "GET":
        return render(
                        request=request,
                        template_name="form.html",
                        context={}
        )
    elif  request.method == "POST":
        name = request.POST["name"]
        report = request.POST["report_text"]
        models.Report.objects.create(name=name,report_text=report)
        return render(
                        request=request,
                        template_name="form.html",
                        context={}
                    )

def statements(request):
    _data = lambda: utils.native_paginate(request, models.Report.objects.all().order_by("-id"), 100) 
    obj = utils.get_cache(f"statements {request.GET.get('page', 1)}", lambda: _data(), timeout=5)  
    return render(
                    request=request,
                    template_name="statements.html",
                    context={"obj":obj}
                )


    

def statement(request,pk: str):
    obj = utils.get_cache(f"statement ", lambda: models.Report.objects.get(id=int(pk)), timeout=2)
    return render(
                    request=request,
                    template_name="statement.html",
                    context={"obj":obj}
                )

def statement_delete(request,pk: str):
    models.Report.objects.get(id=int(pk)).delete()

    return redirect(reverse("statements"))





