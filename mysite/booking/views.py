from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

        try:
            check_in = datetime.strptime(request.POST['check_in'], '%Y-%m-%d').date()
            check_out = datetime.strptime(request.POST['check_out'], '%Y-%m-%d').date()
            valid_prop = []
            guests = int(guests)

            for p in properties:
                bookings = Booking.objects.filter(property_id=p.property_id)
                total_guests = 0
                max = p.size
                for b in bookings:
                    if b.end_date < check_in:
                        continue
                    elif b.start_date > check_out:
                        continue
                    else:
                        total_guests += b.num_guests
                        if total_guests >= max:
                            break
                if total_guests + guests <= max:
                    valid_prop.append(p)
        except ValueError:
            valid_prop = properties

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'search_results.html', {'properties':valid_prop, 'location':location})
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

            #room creation
            property_id = a
            create_rooms(property_id)

            messages.success(request,'Property listed!')
            return redirect('home')

    else: 
        print('NOT VALID')
        form = PropertyCreationForm()
    return render(request,'add_property.html',{'form':form})

def property_view(request, property_id):
    property = Property.objects.get(property_id=property_id)
    rooms = Room.objects.filter(property_id=property_id)
    return render(request, 'property_view.html', {'property':property,'rooms':rooms})

@login_required(login_url='/login')
def book_property_view(request, property_id):
    user = request.user
    p = Property.objects.get(property_id=property_id)
    if request.method == 'POST':
        booking_form = BookingCreationForm(request.POST)
       # print(booking_form.room_number)

        if booking_form.is_valid():
            room_number = booking_form.cleaned_data['room_number']
            room = Room.objects.get(property_id=property_id, room_number=room_number)

            start_date = booking_form.cleaned_data['start_date']
            end_date = booking_form.cleaned_data['end_date']
            num_guests = booking_form.cleaned_data['num_guests']
            
            booking = Booking(user_id=user,start_date=start_date, end_date=end_date, num_guests=num_guests, property_id=p)
            booking.save()
            booking_table = BookingTable(booking=booking, room=room)
            booking_table.save()
           
            messages.success(request,'Property Booked!')
            return redirect('home')

    else: 
        print('NOT VALID')
        booking_form = BookingCreationForm()
        
    return render(request, 'property_booking.html', {'booking_form':booking_form})


#creating rooms
def create_rooms(property):
    size = property.size
    for i in range(size):
        r = Room(room_number=(i+1),property_id=property)
        r.save()
