# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('analysis/<id>/', views.analysis, name='analysis'),
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),

]
