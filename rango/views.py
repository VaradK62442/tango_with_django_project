from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

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

def show_category(request, category_name_slug):
    # create context_dict to pass to template rendering engine
    context_dict = {}

    try:
        # can we find category name with the given slug?
        # if we can't, .get() method raises DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)

        # retrieve all associated pages
        pages = Page.objects.filter(category=category)

        # add results list to the template context under name pages
        context_dict['pages'] = pages
        # add category object from database to context dict
        # use this in template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # template will display "no category" message
        context_dict['category'], context_dict['pages'] = None, None

    return render(request, 'rango/category.html', context=context_dict)
