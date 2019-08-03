from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class DateInput(forms.DateInput):
	input_type = 'date'

class CustomUserCreationForm(UserCreationForm):
	# birthday = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
	# description = forms.CharField(widget=forms.Textarea)

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'birthday', 'description']
		widgets = {'birthday': DateInput(),}


# class CustomUserChangeForm(UserChangeForm):
# 	birthday = forms.DateField(widget=forms.SelectDateWidget)
# 	description = forms.CharField(widget=forms.Textarea)
#
# 	class Meta(UserChangeForm):
# 		model = CustomUser
# 		fields = ['birthday', 'description']

class CustomUserProfileEditForm(forms.ModelForm):
	class Meta(forms.ModelForm):
		model = CustomUser
		fields = ['photo', 'first_name', 'last_name', 'birthday', 'description']
		widgets = {'birthday': DateInput(),}
		labels = {'photo': 'Profile picture URL'}
		help_texts = {'photo': '.jpeg, .jpg, gif or .png images only'}
