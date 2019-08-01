from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from booking.models import Booking, Property
from user_manager.models import *
import json
from datetime import date

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
def profile_view(request, user_id):
    if request.method == 'GET':
        # If viewing the user's own profile
        if (request.user.user_id == int(user_id)):
            return render(request, 'profile.html')

        # Else viewing a stranger's profile
        else:
            user_data = CustomUser.objects.get(user_id=user_id)
            # age = date.today().year - user_data.birthday.year
            return render(request, 'other_profile.html', {'user_data':user_data})
            # return render(request, 'other_profile.html', {'user_data': user_data, 'age': age})
    else:
        return True

@login_required(login_url='/login')
def user_properties_view(request):
	user = request.user
	user_properties_shareable = Property.objects.filter(host_id=user,shareable=True)
	user_properties_unshareable = Property.objects.filter(host_id=user,shareable=False)
	return render(request, 'user_properties.html', {'user_properties_shareable':user_properties_shareable,'user_properties_unshareable':user_properties_unshareable})

@login_required(login_url='/login')
def user_bookings_view(request):
	user = request.user
	bookings = Booking.objects.filter(user_id=user)
	return render(request, 'user_bookings.html', {'bookings':bookings})

@login_required(login_url='/login')
def user_favourites_view(request):
	user = request.user
	favourites = PropertyFavourites.objects.filter(user_id=user)
	return render(request, 'user_favourites.html', {'favourites':favourites})


@login_required(login_url='/login')
def add_to_favourites(request):
	
	property_id = int(request.GET.get('property'))
	# change to get after deleting database
	repeats = PropertyFavourites.objects.filter(property=property_id)
	if repeats:
		response_data = {"result" : "Success", "message" : "Already added to favourites"}
		return HttpResponse(json.dumps(response_data))
	
	property = Property.objects.get(property_id=property_id)
	user = request.user
	print('hello')
	print(type(property))
	favourite = PropertyFavourites(user=user,property=property)
	favourite.save()

	# reponse data probably unecessary, will clean up later
	response_data = {}
	try:
		response_data['result'] = 'Success'
		response_data['message'] = 'Added to favourites!'
	except:
		response_data['result'] = 'Oh no'
		response_data['message'] = 'Try again'
	data = json.dumps(response_data)
	return HttpResponse(data)

@login_required(login_url='/login')
def profile_edit_view(request):
	if request.method == 'POST':
		form = CustomUserProfileEditForm(request.POST)
		if form.is_valid():
			form.save()
			# username = form.cleaned_data.get('username')
			messages.success(request, 'Changes saved')
			return redirect('profile')

	else:
		form = CustomUserProfileEditForm()
		return render(request, 'edit_profile.html', {'form': form})