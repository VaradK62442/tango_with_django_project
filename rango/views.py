from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category

# each view exists here as a series of individual functions
# each view takes in at least one argument - a HttpRequest object
    # conventionally named request
# each view must return a HttpResponse object
    # simple object takes in string param representing content of the page

def index(request):
    # query database for a list of all cateogires currently stored
    # order categories by number of likes, descending
    # retrieve top 5 only, or all if less than 5
    # place list in context_dict that will be passed to template
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # render response and send it back
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'Crunch, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/about.html', context=context_dict)
