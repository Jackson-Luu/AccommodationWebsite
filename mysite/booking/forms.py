from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Property, Booking

class PropertyCreationForm(forms.ModelForm):
    name = forms.CharField(label='Property Name')
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'step': 0.25}))
    location = forms.CharField()
    size = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    bookable = forms.BooleanField()
    class Meta(forms.ModelForm):
        model = Property
        fields = ['name','price','location','size','description','bookable']

class BookingCreationForm(forms.ModelForm):
    # room_number = forms.IntegerField(label='Room Number')
    num_guests = forms.IntegerField(label='Number of Guests')
    start_date = forms.DateField(label='Start Date', required=True,widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='End Date', required=True,widget=forms.SelectDateWidget)
    class Meta(forms.ModelForm):
       model = Booking
       fields = ['start_date','end_date', 'num_guests']
       

# class BookingTableCreationForm(form.ModelForm):
#     room = forms.IntegerField()
#     class Meta(forms.ModelForm):
#         model = BookingTable
#         fields = ['room']

