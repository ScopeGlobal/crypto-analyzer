# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json
import pandas as pd

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

json_data = open('static/assets/users.json')   
data1 = json.load(json_data) # deserialises it
data2 = json.dumps(data1) # json formatted string

json_data.close()


# df_open = pd.read_csv('static/assets/csv/predicted_open_result_rf.csv',names = ['predicted_open']) 
# df_result = pd.read_csv('static/assets/csv/predicted_result_rf.csv', names=['predicted_close'])


@login_required(login_url="/login/")
def index(request):
    data = cg.get_price(ids='bitcoin,litecoin,ethereum,binance coin,tether', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
    return render(request, 'demo.html',{'data':data})

@login_required(login_url="/login/")
def analysis(request,id):
    data = cg.get_price(ids=id, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
    return render(request, 'main.html',{'data':data,'id':id})


@login_required(login_url="/login/")
def contact(request):
    return render(request,'contact.html',{'experts':data1})

@login_required(login_url="/login")
def profile(request):
    return render(request,'profile.html')
