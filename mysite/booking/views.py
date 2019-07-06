from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import PropertyCreationForm
from django.urls import reverse
from .models import Property

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

def add_property_view(request):
    if request.method == 'POST':
        form = PropertyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Property listed!')
            return redirect('home')

    else: 
        print('NOT VALID')
        form = PropertyCreationForm()
    return render(request,'add_property.html',{'form':form})

def search_results_view(request):
    return render(request, 'search_results.html', {})

