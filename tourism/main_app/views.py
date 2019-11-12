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



# Create your views here.
class Index(TemplateView):
    template_name = 'main_app/index.html'


class GetCities(APIView):
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


class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

	def post(self, request):
		city = request.POST.get("city", " ")
		#check_in = request.POST.get("check-in-date", " ")
		#check_out = request.POST.get("check-out-date", " ")
		hotels = list(Hotel.objects.all())
		results = []
		for hotel in hotels:
			hotel = str(hotel)
			if city.lower() in hotel.lower():
				results.append(hotel)
		return render(request, self.template_name, {'results':results})



class LoginPage(TemplateView):
	template_name = 'main_app/login_page.html'
	



