from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from booking.models import Booking, Property
from user_manager.models import *
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from review.models import UserReviews


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
        reviews = list(UserReviews.objects.filter(reviewee=user_id))
        for (i, r) in enumerate(reviews):
            reviews[i] = (reviews[i], r.reviewer.first_name)
        # If viewing the user's own profile
        if request.user.user_id == int(user_id):
            return render(request, 'profile.html', {'reviews': reviews})

        # Else viewing a stranger's profile
        else:
            user_data = CustomUser.objects.get(user_id=user_id)
            # age = date.today().year - user_data.birthday.year
            return render(request, 'other_profile.html', {'user_data': user_data, 'reviews': reviews})
            # return render(request, 'other_profile.html', {'user_data': user_data, 'age': age})
    elif request.method == 'POST':
        UserReviews(reviewer=request.user,reviewee=CustomUser.objects.get(user_id=user_id),rating=request.POST['stars'],text=request.POST['reviewText']).save()
        user_data = CustomUser.objects.get(user_id=user_id)
        reviews = list(UserReviews.objects.filter(reviewee=user_id))
        for (i, r) in enumerate(reviews):
            reviews[i] = (reviews[i], r.reviewer.first_name)        
        return render(request, 'other_profile.html', {'user_data': user_data, 'reviews': reviews})
    else:
        return True


@login_required(login_url='/login')
def user_properties_view(request):
	user = request.user
	user_properties_shareable = Property.objects.filter(host_id=user, shareable=True)
	user_properties_unshareable = Property.objects.filter(host_id=user, shareable=False)
	print(user.user_id)
	return render(request, 'user_properties.html', {'user_properties_shareable': user_properties_shareable,
	                                                'user_properties_unshareable': user_properties_unshareable})


@login_required(login_url='/login')
def user_bookings_view(request):
	user = request.user
	bookings = Booking.objects.filter(user_id=user)
	return render(request, 'user_bookings.html', {'bookings': bookings})


@login_required(login_url='/login')
def user_favourites_view(request):
	user = request.user
	favourites = PropertyFavourites.objects.filter(user_id=user)
	return render(request, 'user_favourites.html', {'favourites': favourites})


@login_required(login_url='/login')
def add_to_favourites(request):
	property_id = int(request.GET.get('property'))
	# change to get after deleting database
	repeats = PropertyFavourites.objects.filter(property=property_id)
	if repeats:
		response_data = {"result": "Success", "message": "Already added to favourites"}
		return HttpResponse(json.dumps(response_data))
	
	property = Property.objects.get(property_id=property_id)
	user = request.user
	print('hello')
	print(type(property))
	favourite = PropertyFavourites(user=user, property=property)
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
	user_data = CustomUser.objects.get(user_id=request.user.user_id)
	if request.method == 'POST':
		form = CustomUserProfileEditForm(request.POST, instance=user_data)
		if form.is_valid():
			form.save()
			messages.success(request, 'Changes saved')
	
	else:
		form = CustomUserProfileEditForm()
	return render(request, 'edit_profile.html', {'form': form, 'user_data': user_data})


@login_required(login_url='/login')
def password_change_view(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Password changed')
			return render(request, 'profile.html')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'change_password.html', {'form': form})
