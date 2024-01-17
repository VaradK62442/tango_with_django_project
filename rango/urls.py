from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
        path('', views.index, name='index'),
        # allows us to call the function url and point to `index` view
        # assume host portion of url has already been stripped away
]
