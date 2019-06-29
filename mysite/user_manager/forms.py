from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	birthday = forms.DateField(widget=forms.SelectDateWidget)
	description = forms.CharField(widget=forms.Textarea)

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'birthday', 'description']


class CustomUserChangeForm(UserChangeForm):
	birthday = forms.DateField(widget=forms.SelectDateWidget)
	description = forms.CharField(widget=forms.Textarea)

	class Meta(UserChangeForm):
		model = CustomUser
		fields = ['birthday', 'description']
