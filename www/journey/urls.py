# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.journey.views',
                       url(r'^$', 'journey_list'),
                       url(r'^write_journey$', 'write_journey'),
                       url(r'(?P<journey_id>\d+)$', 'journey_detail'),
                       )
