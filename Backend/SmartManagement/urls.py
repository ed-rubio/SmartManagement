
''' URL configuration for SmartManagement project.

    The `urlpatterns` list routes URLs to views.
    For more information please see: https://docs.djangoproject.com/en/5.1/topics/http/urls/
'''

from API import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('main/', admin.site.urls),
]