from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
import json
import decimal
from django.forms.models import model_to_dict
import csv
from random import random, randint, shuffle
from .models import CustomUser
from review.models import PropertyReviews
from decimal import Decimal
from django.db import IntegrityError, DataError
from django.core.serializers.json import DjangoJSONEncoder

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
        with open('data/reviews.csv', newline='', encoding="utf-8") as revfile:
            revreader = csv.DictReader(revfile)
            review = next(revreader)
            for idx, row in enumerate(datareader):
                # Number of properties to parse
                if idx > 400:
                    break
                try:
                    user = CustomUser.objects.create_user(username=(row['host_id']+row['host_name']), password='password', first_name=row['host_name'], description=row['host_about'], birthday=date(randint(1960,1999), 1, 1), photo=row['host_picture_url'])
                    p = Property(name=row['name'], host_id=user, price=Decimal(row['price'][1:].replace(",", "")), location=row['city'], size=int(row['accommodates']), description=row['description'], shareable=(random() < 0.5))
                    p.save()

                    amenities = row['amenities'][1:-1].split(",")
                    for am in amenities:
                        try:
                            aobj = Amenity.objects.get(amenity_name = am)
                            PropertyAmenities(property=p, amenity=aobj).save()
                        except Amenity.DoesNotExist:
                            continue

                    PropertyImages(property=p, image=row['picture_url']).save()

                    if p.shareable:
                        rooms = room_gen(p.size, int(row['bedrooms']))
                        if not rooms:
                            p.shareable = False
                            p.save()
                        else:
                            for r in rooms:
                                Room(property_id=p, num_guests=r, price=((p.price / p.size) * r), description="Room Description").save()

                    while(review['listing_id'] == row['id']):
                        try:
                            u = CustomUser.objects.filter(first_name=review['reviewer_name'])[:1].get()
                        except CustomUser.DoesNotExist:
                            u = CustomUser.objects.create_user(username=(review['reviewer_id']+review['reviewer_name']), password='password', first_name=review['reviewer_name'], birthday=date(randint(1960,1999), 1, 1))

                        PropertyReviews(reviewer=u, reviewee=p, rating=randint(3, 5), text=review['comments']).save()
                        review = next(revreader)

                # User already exists
                except IntegrityError:
                    try:
                        Property.objects.get(name=row['name'])
                        continue
                    except Property.DoesNotExist:
                        p = Property(name=row['name'], host_id=CustomUser.objects.get(username=(row['host_id']+row['host_name'])), price=Decimal(row['price'][1:].replace(",", "")), location=row['city'], size=int(row['accommodates']), description=row['description'], shareable=(random() < 0.5))
                        p.save()

                        amenities = row['amenities'][1:-1].split(",")
                        for am in amenities:
                            try:
                                aobj = Amenity.objects.get(amenity_name = am)
                                PropertyAmenities(property=p, amenity=aobj).save()
                            except Amenity.DoesNotExist:
                                continue

                        PropertyImages(property=p, image=row['picture_url']).save()

                        if p.shareable:
                            rooms = room_gen(p.size, int(row['bedrooms']))
                            if not rooms:
                                p.shareable = False
                                p.save()
                            else:
                                for r in rooms:
                                    Room(property_id=p, num_guests=r, price=((p.price / p.size) * r), description="Room Description").save()
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

# Generate rooms for a property
def room_gen(size, num_rooms):
    if num_rooms > size or num_rooms == 0:
        return []
    rooms = []
    rands = []
    r_sum = 0.0
    for r in range(num_rooms - 1):
        rand = random()
        rands.append(rand)
        r_sum += rand
    
    total = size
    for r in rands:
        room = int((r / r_sum) * (size - 1))
        if room == 0:
            room = 1
        rooms.append(room)
        total -= room
    rooms.append(total) 
        
    return rooms

def about_view(request):
    return render(request,'about.html',{})

def home_view(request,*args, **kwargs):
    # CSV call, comment out to improve homepage performance
    if not check_csv():
        load_csv()
    seq = list(range(0, Property.objects.all().count()+1))
    shuffle(seq)
    properties = []
    for i in range(0, 4):
        shuffle(seq)
        x = seq.pop()
        p = Property.objects.all()[x]
        properties.append(p)
    # properties = Property.objects.all()[:4]

    # query an image for each property
    imgs = []
    for p in properties:
        try:
            imgs.append(PropertyImages.objects.filter(property=p.property_id).values_list('image', flat=True)[0])
        except IndexError:
            imgs.append("https://images.unsplash.com/photo-1516156008625-3a9d6067fab5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80")
    return render(request, 'home.html', {'properties':properties, 'images':imgs})

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
            properties = Property.objects.filter(location__iexact=location)
            guests = 0
        else:        
            properties = Property.objects.filter(location__iexact=location, size__gte=guests)
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

                    p_dict['image'] = list(PropertyImages.objects.filter(property=p.property_id).values_list('image', flat=True))
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

                p_dict['image'] = list(PropertyImages.objects.filter(property=p.property_id).values_list('image', flat=True))
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
def add_property_view(request):
    user = request.user
    amenity_list = Amenity.objects.all()
    if request.method == 'POST':
        try:
            shareable = request.POST.get('shareable') 
        except ValueError:
            print("enter valid values")
        
        if shareable == "Yes":
            try:
                property_name = request.POST.get('property_name')
                property_location = request.POST.get('property_location')
                property_description = request.POST.get('property_description')
                checked_amenities = request.POST.getlist('amenities')
            except ValueError:
                print("enter valid values")
            if property_name and property_location and property_description:
                p = Property(host_id=user,name=property_name,location=property_location,description=property_description,shareable=True,bookable=False)
                p.save()
            else:
                return render(request,'add_property.html',{'error': "Please fill in all required fields",'amenity_list':amenity_list})
            for am in checked_amenities:
                aobj = Amenity.objects.get(amenity_id=am)
                PropertyAmenities(property=p, amenity=aobj).save()
            
            return redirect('my_properties')
            
        elif shareable == "No":
            try:
                property_name = request.POST.get('property_name')
                property_location = request.POST.get('property_location')
                property_description = request.POST.get('property_description')
                checked_amenities = request.POST.getlist('amenities')
                property_price = request.POST.get('property_price')
                property_size = request.POST.get('property_size')
            except ValueError:
                print("enter valid values")
            if property_name and property_location and property_description and property_price and property_size:
                p = Property(host_id=user,name=property_name,price=property_price,location=property_location,size=property_size,description=property_description,shareable=False)
                p.save()
            else:
                return render(request,'add_property.html',{'error': "Please fill in all required fields",'amenity_list':amenity_list})

            for am in checked_amenities:
                aobj = Amenity.objects.get(amenity_id=am)
                PropertyAmenities(property=p, amenity=aobj).save()
            
            return redirect('my_properties')
            
    return render(request,'add_property.html',{'amenity_list':amenity_list})

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
        Property.objects.filter(property_id=property_id).update(price=new_price,size=new_size,bookable=True)
        return redirect('my_properties') # redirect to user's property list
    else:
        form = RoomCreationForm()
    return render(request,'add_room.html',{'form':form})

def property_view(request, property_id, check_in=None, check_out=None):
    property = Property.objects.get(property_id=property_id)

    if request.method == 'POST':
        PropertyReviews(reviewer=request.user, reviewee=property, rating=request.POST['stars'], text=request.POST['reviewText']).save()

    rooms = Room.objects.filter(property_id=property_id)
    imgs = list(PropertyImages.objects.filter(property=property_id).values_list('image', flat=True))

    # Find amenities for the property
    amenities = []
    prop_am = PropertyAmenities.objects.filter(property=property)
    for am in prop_am:
        amenities.append(am.amenity.amenity_name)

    # Find reviews for the property
    reviews = list(PropertyReviews.objects.filter(reviewee=property_id))
    for i, r in enumerate(reviews):
        reviews[i] = (reviews[i], r.reviewer.first_name)

    # Find property host
    owner = CustomUser.objects.get(username=property.host_id)
    user = request.user

    # Find property bookings
    bookings = Booking.objects.filter(property_id=property_id)
    blist = []
    room_list = list(Room.objects.filter(property_id=property_id).values_list('room_id', flat=True))
    for b in bookings:
        if b.status == "Accepted":
            if property.shareable:
                room_book = list(BookingTable.objects.filter(booking=b).values_list('room', flat=True))
                booker_id = str(b.user_id.user_id)
                booker = b.user_id.first_name
                for room in room_book:
                    bdict = model_to_dict(b, fields=['start_date', 'end_date'])
                    bdict['room'] = room_list.index(room) + 1
                    bdict['user_id'] = booker_id
                    bdict['user'] = booker
                    blist.append(bdict)
            else:
                blist.append(model_to_dict(b, fields=['start_date', 'end_date']))

    # Convert bookings for Jscript
    bookings = json.dumps(blist, cls=DjangoJSONEncoder)

    return render(request, 'property_view.html', {'property':property,'rooms':rooms, 'amenities':amenities, 'check_in':check_in, 'check_out':check_out, 'images':imgs, 'reviews':reviews, 'owner':owner,'user':user, 'bookings':bookings, 'blist':blist})


@login_required(login_url='/login')
def booking_approvals_view(request):
    user = request.user
    properties = Property.objects.filter(host_id=user.user_id)
    pending_bookings = []
    for p in properties:
        b = Booking.objects.filter(property_id=p.property_id,status='Pending')
        if b:
            b_list = list(b)
            pending_bookings.append(b_list)
        
    return render(request, 'booking_approvals.html', {'pending_bookings':pending_bookings})


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
        if check_in_date and check_out_date:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
            if check_in_date >= check_out_date:
                return render(request, 'booking.html', {
                'error': "Invalid dates.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
                })
        else:
            return render(request, 'booking.html', {
            'error': "Invalid check-in/check-out dates.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
            }) 
       
        if p.shareable == True:

            if not p.bookable:
                return render(request, 'booking.html', {
                'error': "This property is not available for booking at this time.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
                })

            checked_rooms = request.POST.getlist('rooms')
            num_guests = request.POST.get('num_guests')
            if not checked_rooms or not num_guests:
                return render(request, 'booking.html', {
                'error': "Please enter all required fields.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
                })
            
            max_guests = 0
            for r in checked_rooms:
                room_obj = Room.objects.get(room_id=int(r))
                max_guests = max_guests + room_obj.num_guests

            if int(num_guests) > max_guests:
                return render(request, 'booking.html', {
                'error': "Exceeded maximum number of guests.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
                })

            # Check pre-existing bookings for property
            bookings = Booking.objects.filter(property_id=p.property_id)
            for b in bookings:
                if b.status == "Accepted":
                    if b.end_date < check_in_date:
                        continue
                    elif b.start_date > check_out_date:
                        continue
                    else:
                        # Check if booked rooms clashes with selected rooms
                        booked_rooms = list(BookingTable.objects.filter(booking=b).values_list('room', flat=True))
                        if not set([int(i) for i in checked_rooms]).isdisjoint(booked_rooms):
                            return render(request, 'booking.html', {
                            'error': "Room is unavailable for that period.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out})

            booking_instance = Booking(user_id=user,start_date=check_in_date, end_date=check_out_date,property_id=p,num_guests=num_guests,num_rooms=len(checked_rooms))
            booking_instance.save()
            #make booking
            #make booking_table
            for r in checked_rooms:
                room_obj = Room.objects.get(room_id=int(r))
                booking_table_instance = BookingTable(room=room_obj,booking=booking_instance)
                booking_table_instance.save()

            messages.success(request,'Property Booked!')
            return redirect('my_bookings')
            

        elif p.shareable == False:
            num_guests = request.POST.get('num_guests')
            if not num_guests:
                return render(request, 'booking.html', {
                'error': "Please enter all required fields.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
                })

            if int(num_guests) > p.size:
                return render(request, 'booking.html', {
                'error': "Exceeded maximum number of guests.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out 
                })

            # Check pre-existing bookings for property
            bookings = Booking.objects.filter(property_id=p.property_id)
            for b in bookings:
                if b.status == "Accepted":
                    if b.end_date < check_in_date:
                        continue
                    elif b.start_date > check_out_date:
                        continue
                    else:
                        return render(request, 'booking.html', {
                        'error': "Property is unavailable for that period.","property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out})

            booking_instance = Booking(user_id=user,start_date=check_in_date, end_date=check_out_date,property_id=p,num_guests=num_guests)
            booking_instance.save()

            messages.success(request,'Property Booked!')
            return redirect('my_bookings')
       
        
    return render(request, 'booking.html', {"property":p, "rooms":room_list, "check_in":check_in, "check_out":check_out })


@login_required(login_url='/login')
def select_property_type_view(request):

    if request.method == 'POST':
        selection_form = SelectPropertyTypeForm(request.POST)
        if selection_form.is_valid():
            selection = selection_form.cleaned_data['shareable']
            

            if selection == 'True':
                return redirect('add_shareable_property')
            elif selection == 'False':
                 return redirect('add_unshareable_property')
            return redirect('home')
    else:
        selection_form = SelectPropertyTypeForm()

    return render(request, 'select_property_type.html', {'selection_form':selection_form})

@login_required(login_url='/login')
def edit_property_view(request,property_id):
    property = Property.objects.get(property_id=property_id)
    user = request.user
    owner = CustomUser.objects.get(username=property.host_id)
    try:
        property_imgs = PropertyImages.objects.get(property_id = property_id)
    except:
        property_imgs = PropertyImages(property_id=property_id)
        property_imgs.save()
    img_form = PropertyImageURLsForms(request.POST, instance=property_imgs)
    
    if request.method == 'POST':
        if property.shareable == True:
            # print("yes")
            edited_form = ShareablePropertyCreationForm(request.POST,instance=property)
        else:
            edited_form = UnshareablePropertyCreationForm(request.POST,instance=property)
        if edited_form.is_valid():
            edited_form.save()
            f = img_form.save(commit=False)
            f.property_id = property_id
            f.save()
            messages.success(request,'Changes Saved!')
            return redirect('my_properties')
    else:
        if property.shareable == True:
            edited_form = ShareablePropertyCreationForm(instance=property)
        else:
            edited_form = UnshareablePropertyCreationForm(instance=property)
    return render(request,'edit_property.html',{'edited_form':edited_form, 'user':user, 'owner':owner, 'img_form': img_form})

@login_required(login_url='/login')
def property_rooms_view(request, property_id):
    rooms = Room.objects.filter(property_id=property_id)
    property = Property.objects.get(property_id=property_id)
    return render(request, 'view_rooms.html',{'rooms':rooms,'property':property})

@login_required(login_url='/login')
def property_bookings_view(request, property_id):

    bookings = Booking.objects.filter(property_id=property_id,status='Accepted')
    return render(request, 'property_bookings.html',{'bookings':bookings})


@login_required(login_url='/login')
def edit_room_view(request, room_id):
    room = Room.objects.get(room_id=room_id)
    user = request.user
    property = room.property_id
    owner = property.host_id

    if request.method == 'POST':
        edited_form = RoomCreationForm(request.POST,instance=room)
        if edited_form.is_valid():
            edited_form.save()
            messages.success(request,'Changes Saved!')
            return redirect('view_rooms',property.property_id)
    else:
        edited_form = RoomCreationForm(instance=room)
    return render(request, 'edit_room.html', {'user':user,'owner':owner,'edited_form':edited_form,})



@login_required(login_url='/login') 
def get_data_view(request):

    check_in_date = request.GET.get('check_in_data')
    check_out_date = request.GET.get('check_out_data')
    room_ids = json.loads(request.GET.get('room_ids'))
    
    if check_in_date and check_out_date:
        
        check_in = datetime.strptime(str(check_in_date), '%Y-%m-%d').date()
        check_out = datetime.strptime(str(check_out_date), '%Y-%m-%d').date()
        
        room_attr_list = []
        # room_attr_list template - 
        # [{'availability': True, 'room_id': 5, 'booked_user': None}, 
        # {'availability': True, 'room_id': 6, 'booked_user': None}]
        for id in room_ids:
            int_id = int(id)
        
            room_attr = {'room_id':int_id,'availability':True,'booked_user':None}
            room_bookings = BookingTable.objects.filter(room=int_id)
            for rb in room_bookings:
                b = Booking.objects.get(booking_id=rb.booking.booking_id,status='Accepted')
                if not b:
                    continue
                elif b.end_date < check_in:
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

    response_data = {}
    try:
        response_data['result'] = 'Success'
        response_data['message'] = room_attr_list
    except:
        response_data['result'] = 'Oh no'
        response_data['message'] = 'subprocess module did not run the script correctly'
    data = json.dumps(response_data)
    
    return HttpResponse(data)


@login_required(login_url='/login') 
def booking_approval_data(request):

    response_data = {}

    b_id_str = json.loads(request.GET.get('b_id'))
    booking_id = int(b_id_str) 
    booking = Booking.objects.get(booking_id=booking_id)
    if booking:
        booking.status = 'Accepted'
        booking.save()
        response_data['result'] = 'Success'
        response_data['message'] = 'Booking approved.'
    else:
        response_data['result'] = 'Failure'
        response_data['message'] = 'Booking not found'
    
    data = json.dumps(response_data)
    
    return HttpResponse(data)

@login_required(login_url='/login') 
def booking_rejection_data(request):

    response_data = {}

    b_id_str = json.loads(request.GET.get('b_id'))
    booking_id = int(b_id_str) 
    booking = Booking.objects.get(booking_id=booking_id)
    if booking:
        booking.status = 'Rejected'
        booking.save()
        response_data['result'] = 'Success'
        response_data['message'] = 'Booking rejected.'
    else:
        response_data['result'] = 'Failure'
        response_data['message'] = 'Booking not found'
    
    data = json.dumps(response_data)
    
    return HttpResponse(data)

@login_required(login_url='/login') 
def cancel_booking(request):

    response_data = {}

    b_id_str = json.loads(request.GET.get('b_id'))
    booking_id = int(b_id_str) 
    booking = Booking.objects.get(booking_id=booking_id)
    if booking:
        bt_entries = BookingTable.objects.filter(booking_id=booking_id)
        for bt in bt_entries:
            bt.delete()
        booking.delete()

        response_data['result'] = 'Success'
        response_data['message'] = 'Booking removed.'
    else:
        response_data['result'] = 'Failure'
        response_data['message'] = 'Booking not found'
    
    data = json.dumps(response_data)
    
    return HttpResponse(data)