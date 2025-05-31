from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from plant.models import Plant, Category, Tag
from .forms import PlantForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def plants(request):
    q = request.GET.get('q', None)
    category = request.GET.get('category', None)
    tag = request.GET.get('tag', None)

    plants = Plant.objects.all()

    if q:
        plants = plants.filter(title__contains=q)
    if category:
        plants = plants.filter(category__title=category)
    if tag:
        plants = plants.filter(tags__title=tag)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'plant/plant.html', {'plants': plants, 'categories': categories, 'tags': tags, 'selected_category': category, 'selected_tag': tag, 'q': q})

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