# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 50)
	age = models.IntegerField(default = 0)
	email = models.CharField(max_length = 50)
	password = models.CharField(max_length = 50)

	def __str__(self):
		return self.name + " " +self.age

class Hotel(models.Model):
	name = models.CharField(max_length = 50)
	city = models.CharField(max_length = 50)
	country = models.CharField(max_length = 50)
	address = models.CharField(max_length = 100)
	startPrice = models.FloatField(default = 0.0)
	endPrice = models.FloatField(default = 0.0)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return (self.name + " " +self.city + " " + self.country + " " 
		+ self.address)





