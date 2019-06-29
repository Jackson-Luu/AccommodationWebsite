from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.urls import reverse


# Create your views here.
def register_view(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			# username = form.cleaned_data.get('username')
			messages.success(request, 'Account created!')
			return redirect('home')

	else:
		# print('NOT VALID')
		form = CustomUserCreationForm()
	return render(request, 'register.html', {'form': form})
