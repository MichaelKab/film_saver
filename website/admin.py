"""admin"""
from django.contrib import admin
from website.models import Film, Film_with_user

admin.site.register(Film)
admin.site.register(Film_with_user)
# Register your models here.
