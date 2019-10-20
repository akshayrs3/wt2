# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from .models import User, Hotel



# Create your views here.
class Index(TemplateView):
    template_name = 'main_app/index.html'

class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

	def post(self, request):
		data = request.POST.get("search_bar", "")

		list_of_hotels = list(Hotel.objects.all())

		return render(request, self.template_name, {'list_of_hotels':list_of_hotels})
	





class SearchPageAPI(APIView):
	def get(self, request):
		pass


