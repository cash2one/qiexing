# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^login$', 'www.account.views.login'),
                       url(r'^logout$', 'www.account.views.logout'),
                       url(r'^regist$', 'www.account.views.regist'),
                       url(r'^forget_password$', 'www.account.views.forget_password'),
                       url(r'^qiniu_img_return$', 'www.misc.views.qiniu_img_return'),
                       url(r'^save_img$', 'www.misc.views.save_img'),
                       url(r'^crop_img$', 'www.misc.views.crop_img'),

                       url(r'^$', 'www.journey.views.home'),
                       url(r'^account/', include('www.account.urls')),
                       url(r'^journey/', include('www.journey.urls')),
                       url(r'^kit/', include('www.kit.urls')),
                       url(r'^activity/', include('www.activity.urls')),
                       url(r'^sight/', include('www.sight.urls')),
                       url(r'^answer/', include('www.answer.urls')),
                       url(r'^message/', include('www.message.urls')),
                       url(r'^admin/', include('www.admin.urls')),

                       url(r'^n/(?P<nick>.*)$', 'www.account.views.get_user_by_nick'),
                       url(r'^p/(?P<user_id>\w+)?$', 'www.account.views.user_journey'),
                       url(r'^p/(?P<user_id>\w+)/user_answer$', 'www.account.views.user_answer'),

                       url(r'^s/(?P<template_name>.*)$', 'www.misc.views.static_view'),
                       url(r'^(?P<txt_file_name>\w+)\.txt$', 'www.misc.views.txt_view'),
                       url(r'^500$', 'www.misc.views.test500'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
                       # url(r'^admin/', include(admin.site.urls)),

                       url(r'^crossdomain.xml$', direct_to_template, {'template': 'crossdomain.xml'}),
                       )
