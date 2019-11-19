# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
	
from .models import User, Hotel, Session

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm

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

			print("\n\n\n\n",username, password)
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
		print(cities)
		return JsonResponse(list(cities), safe=False)

class SelectionPage(TemplateView):
	template_name = 'main_app/selection_page.html'

	def post(self, request):
		hotel_name = request.POST.get("hotel-name", " ")
		hotel = Hotel.objects.get(name = hotel_name)

		return render(request, self.template_name, {'hotel_name': result})

class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

	def post(self, request):
		city = request.POST.get("city", " ")
		check_in = request.POST.get("check-in-date", " ")
		check_out = request.POST.get("check-out-date", " ")

		# retrieve pk from Session
		Session.objects.filter(pk = 1).update(check_in = check_in)
		Session.objects.filter(pk = 1).update(check_out = check_out)

		print(Session.objects.all(), "\n\n\n\n\n\n\n\n")
		hotels = Hotel.objects.all()

		
		hotels_dict = []
		for hotel in Hotel.objects.values():
			hotels_dict.append(hotel)

		results = []
		for i, hotel in enumerate(hotels.iterator()): 
			if city.lower() in hotel.city.lower():
				results.append(hotels_dict[i])

		print(results)

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



