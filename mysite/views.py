
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect


def home_page(request):
    html = '<html><body>Hello World! Welcome to our Virtual Study Buddy Finding app!</body></html>'
    return HttpResponse(html)

# comment to test Travis-CI
