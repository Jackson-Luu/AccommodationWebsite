from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Property


class CustomUserCreationForm(UserCreationForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username','password1','password2','first_name', 'last_name', 'birthday','description']

class CustomUserChangeForm(UserChangeForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea)
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ['birthday','description']

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
