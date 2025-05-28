from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from plant.models import Plant
from .forms import PlantForm

# Create your views here.
def plants(request):
    q = request.GET.get('q', None)
    plants = ''
    if q is None or q is "":
        plants = Plant.objects.all()
    elif q is not None:
        plants = Plant.objects.filter(title__contains=q)
    return render(request, 'plant/plant.html', {'plants': plants })

def detail(request, slug=None):
    plant = get_object_or_404(Plant, slug=slug)
    return render(request, 'plant/detail.html', locals())

def tags(request, slug=None):
    plants = Plant.objects.filter(tags__slug=slug)
    return render(request, 'plant/plant.html', locals())

def create(request):
    if request.method == "POST":
        form = PlantForm(request.POST)
        if form.is_valid():
            plant = form.save()
            return HttpResponseRedirect(f"/plant/{plant.slug}/")
        else:
            form = PlantForm()
        return render(request, "plant/edit.html", locals())
    
def edit(request, pk=None):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == "POST":
        form = PlantForm(request.POST, instance=plant)
    if form.valid():
        form.save()
        return HttpResponseRedirect("/plant/")
    else:
        form = PlantForm(instance=plant)
    return render(request, "plant/edit.html", locals())