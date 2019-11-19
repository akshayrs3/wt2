from django.contrib.auth.models import User
from django import forms
import datetime

class UserForm(forms.ModelForm):

	#password = forms.CharField(widget=forms.PasswordInput) 

	class Meta:
		model = User
		fields = ['username', 'email', 'password']


class PaymentPage(forms.Form):
	first_name = forms.CharField(label="First Name", max_length=50)
	last_name = forms.CharField(label="Last Name", max_length=50)
	age = forms.IntegerField(label="Age")
	gender = forms.CharField(label="Gender", max_length=1)

	address = forms.CharField(label="Address", max_length=100)
	city = forms.CharField(label="City", max_length=100)
	zipcode = forms.CharField(label="Zip Code", max_length=6)

	check_in = forms.DateField(label="Check-in Date")
	check_out = forms.DateField(label="Check-out Date")

	hotel_name = forms.CharField(label="Hotel Name", max_length=100)

	class Meta:
		fields = ['first_name', 'last_name', 'age']
