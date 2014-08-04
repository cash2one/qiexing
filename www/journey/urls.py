# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.journey.views',
                       url(r'^$', 'journey_list'),
                       )
