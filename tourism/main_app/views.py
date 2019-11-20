# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
	
from .models import User, Hotel

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, PaymentPage

import pandas as pd 
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create your views here.
class UserFormView(TemplateView):
	form_class = UserForm
	template_name = 'main_app/register.html'
	
	#display blank form for new login
	def get(self, request):
		if "username" in request.session:
			del request.session["username"]
			logout(request)

		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	#after submit
	def post(self, request):
		form = UserForm(data=request.POST)

		#print(type(form),form, "123\n\n\n\n")
		un = request.POST.get("username", " ")
		print(request.POST)

		if(form.is_valid()):
			user = form.save(commit=False)#not saved to db yet
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			
			user.set_password(password) #set password 

			user.save()

			#return user if correct

			user = authenticate(username=username, password=password)
			
			if user is not None:
				
				if user.is_active:
					login(request, user)
					request.session['username'] = username
					#refer user as request.user
					return render(request, 'main_app/index.html')

		return render(request, self.template_name, {'form':form})


class PaymentPage(TemplateView):
	form_class = PaymentPage
	template_name = 'main_app/payment_page.html'

	#after submit
	def post(self, request):
		check_in = request.POST.get("check-in", " ")
		check_out = request.POST.get("check-out", " ")
		hotel_name = request.session["hotel_name"]
		room_type = request.POST.get("room-type", " ")
		room_type = room_type[0].upper() + room_type[1:]
		#need to this again cuz they might change dates at the selection page
		request.session["check_in"] = check_in
		request.session["check_out"] = check_out
		request.session["room_type"] = room_type
		#form = self.form_class(data=request.POST)
		
		data_dict = {'hotel_name': hotel_name, 'check_in': check_in, 'check_out': check_out, 
		'room_type': room_type}
		form = self.form_class(data_dict)
		form.fields['hotel_name'].widget.attrs['readonly'] = True
		form.fields['check_in'].widget.attrs['readonly'] = True
		form.fields['check_out'].widget.attrs['readonly'] = True
		return render(request, self.template_name, {'form':form})



class Index(TemplateView):
    template_name = 'main_app/index.html'


class GetCities(APIView):
	# submission throttling
	def get(self, request):
		search = request.GET.get("city", " ")
		print("\n\n\n\n\n", search)

		'''cities = Hotel.objects.city.filter(city__icontains=search)
								print("\n\n\n\n\n", cities)
								return cities'''

		hotels = Hotel.objects.all()
		cities = set()
		for hotel in hotels.iterator():
			if search.lower() in hotel.city.lower():
				cities.add(hotel.city)
		
		return JsonResponse(list(cities), safe=False)

class SelectionPage(TemplateView):
	template_name = 'main_app/selection_page.html'

	def post(self, request):
		hotel_name = request.POST.get("hotel-name", " ")
		
		hotel = Hotel.objects.get(name = hotel_name)

		request.session["hotel_name"] = hotel_name


		sia = SentimentIntensityAnalyzer()
		reviews = hotel.review.split('||')

		pos = neg = neu = 0
		n_review = len(reviews) 
		for review in reviews:
			score = sia.polarity_scores(review)
			if(score['compound'] > 0.2):
				pos += 1
			elif(score['compound'] <= 0.2 and score['compound'] >= -0.2):
				neu += 1
			else:
				neg += 1

		print("\n\n\n", pos, neu, neg, n_review)
		pos = int(pos * 100/ n_review)
		neu = int(neu * 100/ n_review)
		neg = int(neg * 100/ n_review)
		review_scores = {'pos': pos, 'neu': neu, 'neg':neg}



		return render(request, self.template_name, {'hotel': hotel, 'review_scores': review_scores, 'reviews':reviews})

class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

	def post(self, request):
		city = request.POST.get("city", " ")
		check_in = request.POST.get("check-in-date", " ")
		check_out = request.POST.get("check-out-date", " ")
		guests = request.POST.get("guests", " ")

		# setting session
		request.session["check_in"] = check_in
		request.session["check_out"] = check_out
		request.session["guests"] = guests

		hotels = Hotel.objects.all()

		
		hotels_dict = []
		for hotel in Hotel.objects.values():
			hotels_dict.append(hotel)

		results = []
		for i, hotel in enumerate(hotels.iterator()): 
			if city.lower() in hotel.city.lower():
				results.append(hotels_dict[i])


		return render(request, self.template_name, {'results':results, 
			'check_in': check_in, 'check_out': check_out})

class LoginPage(TemplateView):
	template_name = 'main_app/login_page.html'

	def post(self, request):
		username = request.POST.get("username", " ")
		password = request.POST.get("password", " ")
		user = authenticate(username=username, password=password)
			
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['username'] = username
				return render(request, 'main_app/index.html')



		return render(request, self.template_name)



class ThankYouPage(TemplateView):
	template_name = 'main_app/thankyou_page.html'

	def post(self, request):
		name = request.POST.get("first_name", " ") + ' ' + request.POST.get("last_name", " ")
		email = request.POST.get("email", " ")
		hotel_name = request.POST.get("hotel_name", " ")
		room_type = request.POST.get("room_type", " ")
		print("\n\n\n\n", room_type)
		check_in = request.session["check_in"] 
		check_out = request.session["check_out"] 
		guests = request.session["guests"] 

		results = {'name': name, 'email':email, 'hotel_name':hotel_name, 'check_in':check_in, 'check_out':check_out, 
				   'guests':guests, 'room_type':room_type}

		hotel = Hotel.objects.get(name = hotel_name)
		hotel.max_rooms_available = hotel.max_rooms_available - 1
		hotel.save()


		return render(request, self.template_name, {'results':results})

class ReviewPage(TemplateView):
	template_name = "main_app/review.html"

	def post(self, request):
		return render(request, self.template_name)

class ReviewAPI(TemplateView):
	# submission throttling
	template_name = "main_app/index.html"
	def post(self, request):
		review = request.POST.get("review", " ")
		hotel_name = request.session["hotel_name"]
		hotel = Hotel.objects.get(name = hotel_name)
		print("\n\n\n\n", review)
		hotel.review = hotel.review + "|| " + str(review)
		hotel.save()
		return render(request, self.template_name)



