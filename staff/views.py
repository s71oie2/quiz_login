from django.shortcuts import render
from django.views.generic import TemplateView

class DonationView(TemplateView):
    template_name ='staff/donationOrg.html'

class BoardView(TemplateView):
    template_name ='staff/board.html'
