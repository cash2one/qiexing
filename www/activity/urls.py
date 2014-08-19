# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.activity.views',
                       url(r'^$', 'activity_list'),
                       url(r'^(?P<activity_id>\d+)$', 'activity_detail'),
                       url(r'^create_activity$', 'create_activity'),
                       url(r'^modify_activity/(?P<activity_id>\w+)$', 'modify_activity'),
                       url(r'^remove_activity$', 'remove_activity'),
                       url(r'^join_activity$', 'join_activity'),

                       url(r'^set_top$', 'set_top'),
                       url(r'^cancel_top$', 'cancel_top'),
                       )
