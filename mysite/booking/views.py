from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_view(request,*args, **kwargs):
    properties = Property.objects.all()
    return render(request, 'home.html', {'properties':properties})

def search_view(request, *args, **kwargs):
    if request.method == 'POST':
        location = request.POST['location']
        guests = request.POST['guests']
        if not location:
            return render(request, 'search.html', {
                'location_error': "Invalid location.",
            })

        properties = Property.objects.filter(location=location, size__gte=guests)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'search_results.html', {'properties':properties, 'location':location})
    return render(request, 'search.html', {})

@login_required(login_url='/login')
def add_property_view(request):
    user = request.user
    if request.method == 'POST':
        form = PropertyCreationForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.host_id = user
            a.save()
            messages.success(request,'Property listed!')
            return redirect('home')

    else: 
        print('NOT VALID')
        form = PropertyCreationForm()
    return render(request,'add_property.html',{'form':form})

def property_view(request, property_id):
    return render(request, 'property_view.html', {'property_id':property_id})

@login_required(login_url='/login')
def book_property_view(request, property_id):
    user = request.user
    p = Property.objects.get(property_id=property_id)
    if request.method == 'POST':
        form = BookingCreationForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user_id = user
            a.save()
            messages.success(request,'Property Booked!')
            return redirect('home')

    else: 
        print('NOT VALID')
        form = BookingCreationForm()
    return render(request, 'property_booking.html', {'form':form})