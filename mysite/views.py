from django.views.generic import TemplateView
from plant.views import Diary
class HomeView(TemplateView):
    template_name ='home.html'


