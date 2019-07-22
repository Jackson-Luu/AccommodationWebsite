from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
import decimal
from django.forms.models import model_to_dict
import csv
from random import random
from .models import CustomUser
from decimal import Decimal
from django.db import IntegrityError, DataError

# Create your views here.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

# Parse csv data into database
def load_csv():
    with open('data/listings.csv', newline='', encoding="utf-8") as csvfile:
        datareader = csv.DictReader(csvfile)
        for idx, row in enumerate(datareader):
            # Number of properties to parse
            if idx > 1000:
                break
            try:
                user = CustomUser.objects.create_user(username=(row['host_id']+row['host_name']), password='password', first_name=row['host_name'], description=row['host_about'])
                p = Property(name=row['name'], host_id=user, price=Decimal(row['price'][1:].replace(",", "")), location=row['city'], size=row['accommodates'], description=row['description'], shareable=(random() < 0.5))
                p.save()

                amenities = row['amenities'][1:-1].split(",")
                for am in amenities:
                    try:
                        aobj = Amenity.objects.get(amenity_name = am)
                        PropertyAmenities(property=p, amenity=aobj).save()
                    except Amenity.DoesNotExist:
                        continue

            # User already exists
            except IntegrityError:
                try:
                    Property.objects.get(name=row['name'])
                    continue
                except Property.DoesNotExist:
                    p = Property(name=row['name'], host_id=CustomUser.objects.get(username=(row['host_id']+row['host_name'])), price=Decimal(row['price'][1:].replace(",", "")), location=row['city'], size=row['accommodates'], description=row['description'], shareable=(random() < 0.5))
                    p.save()

                    amenities = row['amenities'][1:-1].split(",")
                    for am in amenities:
                        try:
                            aobj = Amenity.objects.get(amenity_name = am)
                            PropertyAmenities(property=p, amenity=aobj).save()
                        except Amenity.DoesNotExist:
                            continue
            except (DataError, Property.MultipleObjectsReturned):
                continue

# Checks if csv has been loaded yet
def check_csv():
    with open('data/listings.csv', newline='', encoding="utf-8") as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            try:
                Property.objects.get(name=row['name'])
                return True
            except Property.DoesNotExist:
                return False


def home_view(request,*args, **kwargs):
    # CSV call, comment out to improve homepage performance
    if not check_csv():
        load_csv()
    properties = Property.objects.all()
    return render(request, 'home.html', {'properties':properties})

def search_view(request, *args, **kwargs):
    if request.method == 'POST':
        location = request.POST['location']
        guests = request.POST['guests']
        check_in = None	
        check_out = None
        if not location:
            return render(request, 'search.html', {
                'location_error': "Invalid location.",
            })

        if not guests:
            properties = Property.objects.filter(location=location)
            guests = 0
        else:        
            properties = Property.objects.filter(location=location, size__gte=guests)
            guests = int(guests)

        valid_prop = []
        try:
            check_in = datetime.strptime(request.POST['check_in'], '%Y-%m-%d').date()
            check_out = datetime.strptime(request.POST['check_out'], '%Y-%m-%d').date()

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
                    am_list = []
                    prop_am = PropertyAmenities.objects.filter(property=p.property_id)
                    for am in prop_am:
                        am_list.append(am.amenity.amenity_name)
                    p_dict = model_to_dict(p)
                    p_dict['amenities'] = am_list
                    valid_prop.append(p_dict)

        # if no dates entered by user
        except ValueError:
            for p in properties:
                am_list = []
                prop_am = PropertyAmenities.objects.filter(property=p.property_id)
                for am in prop_am:
                    am_list.append(am.amenity.amenity_name)
                p_dict = model_to_dict(p)
                p_dict['amenities'] = am_list
                valid_prop.append(p_dict)
        
        # Pass list of all amenities to html
        amenities = Amenity.objects.all()

        # Escape special chars for parsing
        for v in valid_prop:
            v['description'] = v['description'].replace("/","").replace("\\","").replace("\"","").replace("\'","")

        # Convert list of properties results from Python to JavaScript Object Notation (JSON)
        prop_json = json.dumps(list(valid_prop), cls=DecimalEncoder)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'search_results.html', {'properties':valid_prop, 'location':location, 'amenities':amenities, 'prop_json':prop_json, 'check_in':check_in,'check_out':check_out})
    return render(request, 'search.html', {})

@login_required(login_url='/login')
def add_shareable_property_view(request):
    user = request.user
    if request.method == 'POST':
        form = ShareablePropertyCreationForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.host_id = user
            a.shareable = True
            a.save()

            for am in form.cleaned_data['amenities']:
                aobj = Amenity.objects.get(amenity_name = am)
                PropertyAmenities(property=a, amenity=aobj).save()

            #room creation
            property_id = a.property_id
            # create_rooms(property_id)

            messages.success(request,'Property listed!')
            # add_room_view(request)
            return redirect('add_room',property_id)

    else: 
        form = ShareablePropertyCreationForm()
    return render(request,'add_property.html',{'form':form})


@login_required(login_url='/login')
def add_unshareable_property_view(request):
    user = request.user
    if request.method == 'POST':
        form = UnshareablePropertyCreationForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.host_id = user
            a.size = form.cleaned_data['size']
            a.price = form.cleaned_data['price']
            a.shareable = False
            a.save()

            for am in form.cleaned_data['amenities']:
                aobj = Amenity.objects.get(amenity_name = am)
                PropertyAmenities(property=a, amenity=aobj).save()

            #room creation
            property_id = a
            # create_rooms(property_id)

            messages.success(request,'Property listed!')
            # add_room_view(request)
            return redirect('home')

    else: 
        form = UnshareablePropertyCreationForm()
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
        return redirect('my_properties') # redirect to user's property list
    else:
        form = RoomCreationForm()
    return render(request,'add_room.html',{'form':form})

def property_view(request, property_id, check_in=None, check_out=None):
    property = Property.objects.get(property_id=property_id)
    rooms = Room.objects.filter(property_id=property_id)
    return render(request, 'property_view.html', {'property':property,'rooms':rooms, 'check_in':check_in, 'check_out':check_out})

# @login_required(login_url='/login')
# def book_property_view(request, property_id, check_in=None, check_out=None):
#     user = request.user
#     p = Property.objects.get(property_id=property_id)
#     room_list = Room.objects.filter(property_id=property_id)
#     room_ids = []
#     for r in room_list:
#         room_ids.append(r.room_id)
#     room_num = p.size
#     print(room_num)
    
#     if request.method == 'POST':
        
#         booking_form = BookingCreationForm(request.POST,room_ids=room_ids,check_in=check_in)
        
#         if booking_form.is_valid():    
        
#             start_date = booking_form.cleaned_data['start_date']
#             end_date = booking_form.cleaned_data['end_date']
#             num_guests = booking_form.cleaned_data['num_guests']
#             rooms = booking_form.cleaned_data['rooms']
#             print(rooms)
#             num_rooms = len(rooms)

#             booking_instance = Booking(user_id=user,start_date=start_date, end_date=end_date,property_id=p,num_guests=num_guests,num_rooms=num_rooms)
#             booking_instance.save()
#             #make booking
#             #make booking_table
#             for r in rooms:
#                 room_obj = Room.objects.get(room_id=int(r))
#                 booking_table_instance = BookingTable(room=room_obj,booking=booking_instance)
#                 booking_table_instance.save()

#             messages.success(request,'Property Booked!')
#             return redirect('home')

#     else: 
#         booking_form = BookingCreationForm(room_ids=room_ids,check_in=check_in)
        
#     return render(request, 'property_booking.html', {'booking_form':booking_form})

@login_required(login_url='/login')
def booking_view(request, property_id, check_in=None, check_out=None):
    user = request.user
    p = Property.objects.get(property_id=property_id)
    room_list = Room.objects.filter(property_id=property_id)
    if check_in:
        check_in = str(check_in)
    if check_out:
        check_out = str(check_out)
    
    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date') 
        check_out_date = request.POST.get('check_out_date') 
        if check_in_date:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        else:
            return render(request, 'booking.html', {
            'error': "Invalid check in date.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
            }) 
        if check_out_date:
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        else:
            return render(request, 'booking.html', {
            'error': "Invalid check out date.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
            })   
        if check_in_date and check_out_date:
            if check_in_date > check_out_date:
                return render(request, 'booking.html', {
            'error': "Invalid dates.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
            })
        
        
        rooms = request.POST.getlist('rooms')
        num_guests = request.POST.get('num_guests')
        if not rooms or not num_guests:
            return render(request, 'booking.html', {
            'error': "Please enter all required fields.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
            })
       
        max_guests = 0
        for r in rooms:
            room_obj = Room.objects.get(room_id=int(r))
            max_guests = max_guests + room_obj.num_guests

        if int(num_guests) > max_guests:
            return render(request, 'booking.html', {
            'error': "Exceeded maximum number of guests","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
            })
        booking_instance = Booking(user_id=user,start_date=check_in_date, end_date=check_out_date,property_id=p,num_guests=num_guests,num_rooms=len(rooms))
        booking_instance.save()
        #make booking
        #make booking_table
        for r in rooms:
            room_obj = Room.objects.get(room_id=int(r))
            booking_table_instance = BookingTable(room=room_obj,booking=booking_instance)
            booking_table_instance.save()

        messages.success(request,'Property Booked!')
        return redirect('home')
    return render(request, 'booking.html', {"property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out })


@login_required(login_url='/login')
def select_property_type_view(request):

    if request.method == 'POST':
        selection_form = SelectPropertyTypeForm(request.POST)
        if selection_form.is_valid():
            selection = selection_form.cleaned_data['shareable']
            print(selection)

            if selection == 'True':
                return redirect('add_shareable_property')
            elif selection == 'False':
                 return redirect('add_unshareable_property')
            return redirect('home')
    else:
        selection_form = SelectPropertyTypeForm()
    # selection = selection_form.cleaned_data['shareable']
    # print(selection)
   

    return render(request, 'select_property_type.html', {'selection_form':selection_form})

@login_required(login_url='/login')
def edit_property_view(request,property_id):
    property = Property.objects.get(property_id=property_id)
    if request.method == 'POST':
        edited_form = UnshareablePropertyCreationForm(request.POST,instance=property)
        if edited_form.is_valid():
            edited_form.save()
            return redirect('home')
    else:
        edited_form = UnshareablePropertyCreationForm(instance=property)
    return render(request,'edit_property.html',{'edited_form':edited_form})

@login_required(login_url='/login') 
def get_data_view(request):

    check_in_date = request.GET.get('check_in_data')
    check_out_date = request.GET.get('check_out_data')
    room_ids = json.loads(request.GET.get('room_ids'))

    if check_in_date is not None and check_out_date is not None:
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        
        room_attr_list = []
        # room_attr_list template - 
        # [{'availability': True, 'room_id': 5, 'booked_user': None}, 
        # {'availability': True, 'room_id': 6, 'booked_user': None}]
        for id in room_ids:
            int_id = int(id)
        
            room_attr = {'room_id':int_id,'availability':True,'booked_user':None}
            room_bookings = BookingTable.objects.filter(room=int_id)
            for rb in room_bookings:
                b = Booking.objects.get(booking_id=rb.booking.booking_id)
                if b.end_date < check_in:
                        continue
                elif b.start_date > check_out:
                        continue
                else:
                    booked_user_id = b.user_id.user_id
                    room_attr['availability'] = False
                    room_attr['booked_user'] = booked_user_id
                    break
            room_attr_list.append(room_attr)
        
    else:
        room_attr_list = []
        # print('no dates')
    # print(room_attr_list)
    response_data = {}
    try:
        response_data['result'] = 'Success'
        response_data['message'] = room_attr_list
    except:
        response_data['result'] = 'Oh no'
        response_data['message'] = 'subprocess module did not run the script correctly'
    data = json.dumps(response_data)
    
    return HttpResponse(data)