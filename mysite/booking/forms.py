from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Property, Booking, Room

class DateInput(forms.DateInput):
	input_type = 'date'

class PropertyCreationForm(forms.ModelForm):
	name = forms.CharField(label='Property Name')
	# price = forms.DecimalField(widget=forms.NumberInput(attrs={'step': 0.25}))
	location = forms.CharField()
	# size = forms.IntegerField()
	description = forms.CharField(widget=forms.Textarea)
	bookable = forms.BooleanField()
	class Meta(forms.ModelForm):
		model = Property
		fields = ['name','location','description','bookable']

# class BookingCreationForm(forms.ModelForm):
#     # room_number = forms.IntegerField(label='Room Number')
#     num_guests = forms.IntegerField(label='Number of Guests')
#     start_date = forms.DateField(label='Start Date', required=True,widget=forms.SelectDateWidget)
#     end_date = forms.DateField(label='End Date', required=True,widget=forms.SelectDateWidget)
#     class Meta(forms.ModelForm):
#        model = Booking
#        fields = ['start_date','end_date', 'num_guests']

class BookingCreationForm(forms.Form):

	def __init__(self,*args,room_ids,**kwargs):
		super(BookingCreationForm,self).__init__(*args,**kwargs)
		options=[]
		i = 1
		for r in room_ids:
			options.append((r,'Room ' + str(i)))
			i=i+1

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
