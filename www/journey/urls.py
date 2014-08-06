# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('www.journey.views',
                       url(r'^$', 'journey_list'),
                       url(r'^(?P<journey_id>\d+)$', 'journey_detail'),
                       url(r'^write_journey$', 'write_journey'),
                       url(r'^modify_journey/(?P<journey_id>\w+)$', 'modify_journey'),

                       url(r'^like_journey$', 'like_journey'),
                       url(r'^remove_journey$', 'remove_journey'),

                       url(r'^set_important$', 'set_important'),
                       url(r'^cancel_important$', 'cancel_important'),
                       )
