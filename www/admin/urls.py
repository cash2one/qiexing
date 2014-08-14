# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.admin.views',
                       url(r'^$', 'home'),
                       )


# 提问
urlpatterns += patterns('www.admin.views_sight',

                        url(r'^sight/get_province_by_name$', 'get_province_by_name'),
                        url(r'^sight/get_sight_by_id$', 'get_sight_by_id'),
                        url(r'^sight/modify_sight$', 'modify_sight'),
                        url(r'^sight/remove_sight$', 'remove_sight'),
                        url(r'^sight/add_sight$', 'add_sight'),
                        url(r'^sight/search$', 'search'),
                        url(r'^sight$', 'sight'),
                        )
