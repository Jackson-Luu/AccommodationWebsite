from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Property




class PropertyCreationForm(forms.ModelForm):
    name = forms.CharField(label='Property Name')
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'step': 0.25}))
    location = forms.CharField()
    size = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    bookable = forms.BooleanField()
    class Meta(forms.ModelForm):
        model = Property
        fields = ['name','price','location','size','description','bookable']
