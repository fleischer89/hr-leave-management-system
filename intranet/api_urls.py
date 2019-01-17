__author__ = 'Paul Fleischer'


from django.conf.urls import *
from django.contrib import admin
from intranet.views import *


urlpatterns = [
    # ------- APIs -------- #
    url(r'^chart.json/?$', get_chart_data, name='get_chart_data'),
    url(r'^chart/frequency/options.json/?$', get_chart_frequency_options, name='get_chart_frequency_options'),
]
