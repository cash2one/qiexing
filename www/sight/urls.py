# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.sight.views',
                       url(r'^$', 'sight_map'),
                       url(r'^(?P<sight_id>\d+)$', 'sight_detail'),
                       )
