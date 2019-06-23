from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
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


