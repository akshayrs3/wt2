# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
# class Session(models.Model):
# 	check_in = models.DateField(default=datetime.now())
# 	check_out = models.DateField(default=datetime.now())

# 	def __str__(self):
# 		return (str(self.pk))

class User(models.Model):
	name = models.CharField(max_length=50)
	age = models.IntegerField(default=0)
	email = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	def __str__(self):
		return self.name + " " +self.age

class Hotel(models.Model):
	name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	startPrice = models.FloatField(default=0.0)
	endPrice = models.FloatField(default=0.0)
	image_url = models.CharField(default="empty", max_length=100)
	review = models.CharField(default="empty", max_length=1000000000)
	max_rooms_available = models.IntegerField(default = 20)

	def __str__(self):
		return (self.name + " " +self.city + " " + self.country + " " 
		+ self.address)





