# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import User, Hotel, Session

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Session)
