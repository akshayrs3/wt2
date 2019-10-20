# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

class Index(TemplateView):
    template_name = 'main_app/index.html'

class SearchPage(TemplateView):
	template_name = 'main_app/search_page.html'

