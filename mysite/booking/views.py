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
            # create_rooms(property_id)

            messages.success(request,'Property listed!')
            # add_room_view(request)
            return redirect('home')

    else: 
        form = PropertyCreationForm()
    return render(request,'add_property.html',{'form':form})

@login_required(login_url='/login')
def add_room_view(request,property_id):
    p = Property.objects.get(property_id=property_id)
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        instance = form.save(commit=False)
        instance.property_id = p
        instance.save()
        price = instance.price
        new_price = p.price + price
        new_size = p.size + 1
        #updating property total price
        Property.objects.filter(property_id=property_id).update(price=new_price,size=new_size)
        return redirect('property',p.property_id) # redirect to user's property list
    else:
        form = RoomCreationForm()
    return render(request,'add_room.html',{'form':form})

def property_view(request, property_id):
    property = Property.objects.get(property_id=property_id)
    rooms = Room.objects.filter(property_id=property_id)
    return render(request, 'property_view.html', {'property':property,'rooms':rooms})

@login_required(login_url='/login')
def book_property_view(request, property_id):
    user = request.user
    p = Property.objects.get(property_id=property_id)
    room_list = Room.objects.filter(property_id=property_id)
    room_ids = []
    for r in room_list:
        room_ids.append(r.room_id)
    room_num = p.size
    print(room_num)
    
    if request.method == 'POST':
        
        booking_form = BookingCreationForm(request.POST,room_ids=room_ids)
        
        if booking_form.is_valid():    
        
            start_date = booking_form.cleaned_data['start_date']
            end_date = booking_form.cleaned_data['end_date']
            num_guests = booking_form.cleaned_data['num_guests']
            rooms = booking_form.cleaned_data['rooms']
            print(rooms)
            num_rooms = len(rooms)

            booking_instance = Booking(user_id=user,start_date=start_date, end_date=end_date,property_id=p,num_guests=num_guests,num_rooms=num_rooms)
            booking_instance.save()
            #make booking
            #make booking_table
            for r in rooms:
                room_obj = Room.objects.get(room_id=int(r))
                booking_table_instance = BookingTable(room=room_obj,booking=booking_instance)
                booking_table_instance.save()

            messages.success(request,'Property Booked!')
            return redirect('home')

    else: 
        booking_form = BookingCreationForm(room_ids=room_ids)
        
    return render(request, 'property_booking.html', {'booking_form':booking_form})

