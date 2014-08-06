# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.activity.views',
                       url(r'^$', 'activity_list'),
                       url(r'^(?P<activity_id>\d+)$', 'activity_detail'),
                       url(r'^launch_activity$', 'launch_activity'),
                       )
