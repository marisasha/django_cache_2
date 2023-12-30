import datetime
import sqlite3
import time

from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from django.core.cache import caches

RamCache = caches["default"]

def get_cache(key: str, query: callable = lambda: any, timeout: int = 10, cache: any = RamCache) -> any:
    data = cache.get(key)
    if data is None:
        data = query()
        cache.set(key, data, timeout)
    return data


def native_paginate(request, object_list, per_page):
    selected_page = request.GET.get(key="page", default=1)
    page_objs = Paginator(object_list=object_list, per_page=per_page)
    page_obj = page_objs.page(number=selected_page)
    return page_obj