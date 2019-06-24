from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import CustomUserCreationForm
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            messages.success(request,'Account created!')
            return redirect('home')

    else: 
        print('NOT VALID')
        form = CustomUserCreationForm()
    return render(request, 'register.html',{'form':form})

def home_view(request,*args, **kwargs):
    return render(request, 'home.html', {})

def search_view(request, *args, **kwargs):
    if request.method == 'POST':
        location = request.POST['location']
        print(location)
        if not location:
            return render(request, 'search.html', {
                'location_error': "Invalid location.",
            })
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect('search')
    return render(request, 'search.html', {})

