from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from plant.models import Plant, Category, Tag, PlantFavorite
from .forms import PlantForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

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

def detail_condition(request, slug=None):
    plant = get_object_or_404(Plant, slug=slug)
    return render(request, 'plant/detail_condition.html', locals())

def detail_care(request, slug=None):
    plant = get_object_or_404(Plant, slug=slug)
    return render(request, 'plant/detail_care.html', locals())

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

@require_POST
@login_required
def favorite(request, id):
    plant = get_object_or_404(Plant, id=id)
    favorite = plant.favorite_users.filter(id=request.user.id).first()
    
    if favorite:
        PlantFavorite.objects.get(user=request.user, plant=plant).delete()
        messages.success(request, f'已取消收藏 {plant.title}')
    else:
        PlantFavorite(user=request.user, plant=plant).save()
        messages.success(request, f'已收藏 {plant.title}')
    
    # Redirect back to the previous page
    return HttpResponseRedirect(f"/plant/{plant.slug}/")

@login_required
def favorite_list(request):
    plants = Plant.objects.filter(favorite_users=request.user)
    return render(request, 'plant/favorite_list.html', {'plants': plants})