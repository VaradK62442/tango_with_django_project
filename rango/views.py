from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

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
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

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
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # a HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # provided with valid form?
        if form.is_valid():
            # save new category to the database
            form.save(commit=True)
            # redirect user to index view
            return redirect('/rango/')
        else:
            # supplied form contains errors
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # cannot add page to category that does not exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                # reverse looks up URL names in urls.py
                # if match is found, complete url is returned
                return redirect(reverse('rango:show_category', 
                    kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # bool for telling template if registration was successful
    # false by default, changes to true when registration was successful
    registered = False

    # if POST, process form data
    if request.method == "POST":
        # grab info from raw form information
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save user's form data to database
            user = user_form.save()

            # hash password, update user object
            user.set_password(user.password)
            user.save()

            # sort out UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            # invalid form(s)
            print(user_form.errors, profile_form.errors)

    else:
        # render form
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})

def user_login(request):
    if request.method == "POST":
        # gather username and password
        # user .get since it returns None if value dne
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate
        user = authenticate(username=username, password=password)

        # if user is None, failed auth
        if user:
            # is account active?
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # inactive - no logging in
                return HttpResponse("Your Rango account is disabled.")
        else:
            # invalid login details
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
