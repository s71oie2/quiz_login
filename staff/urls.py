from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('board/', BoardView.as_view(), name='board'),
    path('donation/', DonationView.as_view(), name='donation'),
]