# dj_razorpay/urls.py

from django.contrib import admin
from django.urls import path
from payment import views

urlpatterns = [
	path('payment/<id>/', views.payment, name='payment'),
	path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
