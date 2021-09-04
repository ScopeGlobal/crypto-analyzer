# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from pycoingecko.pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


@login_required(login_url="/login/")
def index(request):
    data = cg.get_price(ids='bitcoin,litecoin,ethereum,binance coin,tether', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
    return render(request, 'demo.html',{'data':data})

@login_required(login_url="/login/")
def analysis(request,id):
    data = cg.get_price(ids=id, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
    id = 'bitcoin'
    return render(request, 'main.html',{'data':data,'id':id})


@login_required(login_url="/login/")
def contact(request):
    experts = [{'id':1,'name':'Harsh','fees':'2000','number':3,'experience':'10 years'}]
    return render(request,'contact.html',{'experts':experts})
