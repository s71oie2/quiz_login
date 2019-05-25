from django.shortcuts import render
from django.views.generic import TemplateView

class PlantView(TemplateView):
    template_name ='plant/plant.html'
