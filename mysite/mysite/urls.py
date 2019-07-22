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
	path('', home_view, name='home'),
	path('search/', search_view),
	path('signup/', register_view),
	path('addshareableproperty/', add_shareable_property_view,name='add_shareable_property'),
    path('addunshareableproperty/', add_unshareable_property_view,name='add_unshareable_property'),
    path('property/<int:property_id>/', property_view, name='property'),
    path('property/<int:property_id>/<check_in>/<check_out>/', property_view, name='property'),
	path('', include('django.contrib.auth.urls')),
	path('profile/', profile_view),
    # path('bookproperty/<int:property_id>/', book_property_view, name='book_property'),
    # path('bookproperty/<int:property_id>/<check_in><check_out>', book_property_view, name='book_property'),
    path('addroom/<int:property_id>/', add_room_view, name='add_room'),
    path('profile/myproperties', user_properties_view, name='my_properties'),
    path('profile/mybookings',user_bookings_view, name='my_bookings'),
    path('selectpropertytype/',select_property_type_view, name='select_property_type'),
    path('changeproperty/<int:property_id>/',edit_property_view, name='edit_property'),


    path('book/<int:property_id>/', booking_view, name='booking'),
    path('book/<int:property_id>/<check_in>/<check_out>/', booking_view, name='booking'),
    path('getdata/', get_data_view, name='getdata'),
    path('addtofavourites/', add_to_favourites, name='favourites'),
    path('profile/myfavourites',user_favourites_view, name='my_favourites'),
	path('edit_profile/', profile_edit_view, name='edit_profile'),
]
