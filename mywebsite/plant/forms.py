from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Plant
from django.forms import ModelForm
class PlantForm(ModelForm):
    title = forms.CharField(label="title",
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model = Plant
        fields = ["title"] 