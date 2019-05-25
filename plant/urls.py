from django.urls import path
from plant import views
from .views import *

app_name = 'plant'

urlpatterns = [
    path('', PlantView.as_view(), name='index'),
]
