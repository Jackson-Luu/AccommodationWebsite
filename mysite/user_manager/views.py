from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from booking.models import Booking, Property
from user_manager.models import CustomUser

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

@login_required(login_url='/login')
def profile_view(request):
	if request.method == 'GET':
		# TODO
		user = request.user
		user_data = CustomUser.objects.filter(user_id = user.user_id)
		return render(request, 'profile.html', {'user_data':user_data})
	else:
		return True

@login_required(login_url='/login')
def user_properties_view(request):
	user = request.user
	user_properties_shareable = Property.objects.filter(host_id=user,shareable=True)
	user_properties_unshareable = Property.objects.filter(host_id=user,shareable=False)
	return render(request, 'user_properties.html', {'user_properties_shareable':user_properties_shareable,'user_properties_unshareable':user_properties_unshareable})
