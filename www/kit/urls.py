# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('www.kit.views',
                       url(r'^$', 'kit_list'),
                       url(r'^(?P<kit_id>\d+)$', 'kit_detail'),
                       url(r'^write_kit$', 'write_kit'),
                       url(r'^modify_kit/(?P<kit_id>\w+)$', 'modify_kit'),

                       url(r'^like_kit$', 'like_kit'),
                       url(r'^remove_kit$', 'remove_kit'),

                       url(r'^set_top$', 'set_top'),
                       url(r'^cancel_top$', 'cancel_top'),
                       )
