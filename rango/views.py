from django.shortcuts import render
from django.http import HttpResponse

# each view exists here as a series of individual functions
# each view takes in at least one argument - a HttpRequest object
    # conventionally named request
# each view must return a HttpResponse object
    # simple object takes in string param representing content of the page

def index(request):
    return HttpResponse("Rango says hey there partner!\n<a href='/rango/about/'>About</a>")


def about(request):
    return HttpResponse("Rango says here is the about page.\n<a href='/rango/'>Index</a>")
