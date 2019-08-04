from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class DateInput(forms.DateInput):
	input_type = 'date'

class ShareablePropertyCreationForm(forms.ModelForm):
    name = forms.CharField(label='Property Name')
    location = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    amenities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=zip(list(Amenity.objects.all().values_list('amenity_name', flat=True)), Amenity.objects.all().values_list('amenity_name', flat=True)), required=True)
    class Meta(forms.ModelForm):
        model = Property
        fields = ['name','location','description']

class UnshareablePropertyCreationForm(forms.ModelForm):
    name = forms.CharField(label='Property Name')
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'step': 0.25}))
    location = forms.CharField()
    size = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    amenities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=zip(list(Amenity.objects.all().values_list('amenity_name', flat=True)), Amenity.objects.all().values_list('amenity_name', flat=True)), required=True)
    class Meta(forms.ModelForm):
        model = Property
        fields = ['name','location','description']

class BookingCreationForm(forms.ModelForm):
    # room_number = forms.IntegerField(label='Room Number')
    num_guests = forms.IntegerField(label='Number of Guests')
    start_date = forms.DateField(label='Start Date', required=True,widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='End Date', required=True,widget=forms.SelectDateWidget)
    class Meta(forms.ModelForm):
       model = Booking
       fields = ['start_date','end_date', 'num_guests']

class BookingCreationForm(forms.Form):

	def __init__(self,room_ids,check_in,*args,**kwargs):
		super(BookingCreationForm,self).__init__() 
		options=[]
		i = 1
		for r in room_ids:
			options.append((r,'Room ' + str(i)))
			i=i+1
           
        # print(check_in)
        # print(kwargs)
        # self.a = 2
		self.fields['rooms'].choices = options
        
	rooms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
	start_date = forms.DateField(label='Start Date', required=True,widget=DateInput())
	end_date = forms.DateField(label='End Date', required=True,widget=DateInput())
	num_guests = forms.IntegerField(label='Number of Guests')




class RoomCreationForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Room
        fields = ['num_guests','price','description']

class SelectPropertyTypeForm(forms.Form):
    CHOICES = [('True','Yes'),('False','No')]
    shareable = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Do you want this property to be shareable?')
    # def __init__(self,*args,**kwargs):
    #     super(SelectPropertyTypeForm,self).__init__(*args,**kwargs)

class PropertyImageURLsForms(forms.ModelForm):
	
	class Meta(forms.ModelForm):
		model = PropertyImages
		fields = ['image']
		labels = {'image': 'Image URL'}
		