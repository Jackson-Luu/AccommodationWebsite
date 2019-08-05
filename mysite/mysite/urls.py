"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from booking.views import *
from user_manager.views import *

urlpatterns = [
	path('admin/', admin.site.urls),
    path('about/',about_view, name='about'),
	path('privacy/', privacy_view, name='privacy'),
	path('', home_view, name='home'),
	path('search/', search_view),
	path('signup/', register_view, name='signup'),

    path('property/<int:property_id>/', property_view, name='property'),
    path('property/<int:property_id>/<check_in>/<check_out>/', property_view, name='property'),
	path('', include('django.contrib.auth.urls')),
    path('profile/<str:user_id>/', profile_view, name='profile'),
    
    path('addroom/<int:property_id>/', add_room_view, name='add_room'),
    path('viewrooms/<int:property_id>/', property_rooms_view, name='view_rooms'),
    path('profile/myproperties', user_properties_view, name='my_properties'),
    path('profile/mybookings',user_bookings_view, name='my_bookings'),
    
    path('<int:property_id>/editproperty/',edit_property_view, name='edit_property'),
    path('<int:room_id>/editroom/',edit_room_view, name='edit_room'),
    
    path('addproperty/',add_property_view, name='add_property'),
    path('mybookingapprovals/',booking_approvals_view, name='booking_approvals'),

    path('cancel_booking/',cancel_booking,name='cancel_booking'),


    path('propertybookings/<int:property_id>/',property_bookings_view,name='property_bookings'),
    path('book/<int:property_id>/', booking_view, name='booking'),
    path('book/<int:property_id>/<check_in>/<check_out>/', booking_view, name='booking'),
    path('getdata/', get_data_view, name='getdata'),
    path('booking_approval_data/',booking_approval_data, name='booking_approval_data'),
    path('booking_rejection_data/',booking_rejection_data, name='booking_rejection_data'),
    path('addtofavourites/', add_to_favourites, name='favourites'),
    path('profile/myfavourites',user_favourites_view, name='my_favourites'),
	path('profile/edit', profile_edit_view, name='edit_profile'),
	path('profile/changepassword', password_change_view, name='change_password')
]
