from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
        path('', views.index, name='index'),
        # allows us to call the function url and point to `index` view
        # assume host portion of url has already been stripped away

        path('about/', views.about, name='about'),
        # map about to about page

        path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
        # map to appropriate category

        path('add_category/', views.add_category, name='add_category'),

        path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),

        path('register/', views.register, name='register'),

        path('login/', views.user_login, name='login'),

        path('restricted/', views.restricted, name='restricted'),

        path('logout/', views.user_logout, name='logout'),
]
