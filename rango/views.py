from django.shortcuts import render
from django.http import HttpResponse

# each view exists here as a series of individual functions
# each view takes in at least one argument - a HttpRequest object
    # conventionally named request
# each view must return a HttpResponse object
    # simple object takes in string param representing content of the page

def index(request):
    # construct dict to pass to template engine as context
    # note the key matches template value
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # return rendered response to send to client
    # make use of shortcut function render
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page.\n<a href='/rango/'>Index</a>")
