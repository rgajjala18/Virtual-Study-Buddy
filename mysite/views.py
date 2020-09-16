
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect


def home_page(request):
    html = '"<html><body>Hello World.</body></html>"'
    return HttpResponse(html)