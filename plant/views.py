from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from plant.models import *
from plant.forms import *
from django.shortcuts import redirect

class PlantView(TemplateView):
    template_name ='plant/plant.html'

def diaryview(request, pk, seed):
    plant = Diary.objects.get(user_id=pk)
    photo = SeedState.objects.get(growth_id=1, seed_id=seed)
    form = PlantForm(request.POST, instance=plant)
    if form.is_valid():
        plant = form.save(commit=True)
        plant.save()
        if plant.exp <= 5:
            plant =  Diary.objects.get(user_id=pk)
            photo = SeedState.objects.get(growth_id=1, seed_id=seed)
        elif plant.exp <= 10:
            plant =  Diary.objects.get(user_id=pk)
            photo = SeedState.objects.get(growth_id=2, seed_id=seed)
        elif plant.exp <= 15:
            plant =  Diary.objects.get(user_id=pk)
            photo = SeedState.objects.get(growth_id=3, seed_id=seed)
        elif plant.exp <= 20:
            plant = Diary.objects.get(user_id=pk)
            photo = SeedState.objects.get(growth_id=4, seed_id=seed)
        else:  # 다 자랐을 때
            plant = Diary.objects.get(user_id=pk)
            photo = SeedState.objects.get(growth_id=1, seed_id=seed)
            return render(request, 'plant/userplant.html', {'plant': plant, 'photo':photo})
    else:
        form = PlantForm(instance=plant)
        # return redirect('home')
    return render(request, 'plant/userplant.html', {'form': form, 'plant': plant, 'photo':photo})
