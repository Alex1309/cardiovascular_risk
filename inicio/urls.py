from django.urls import path
#now import the views.py file into this code
from . import views
from .views import *

app_name = 'inicio'
urlpatterns=[
    path('', geeks_view ),
]