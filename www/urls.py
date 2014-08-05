# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^login$', 'www.account.views.login'),
                       url(r'^logout$', 'www.account.views.logout'),
                       url(r'^regist$', 'www.account.views.regist'),
                       url(r'^forget_password$', 'www.account.views.forget_password'),

                       url(r'^$', 'www.journey.views.home'),
                       url(r'^journey/', include('www.journey.urls')),
                       url(r'^activity/', include('www.activity.urls')),
                       url(r'^sight/', include('www.sight.urls')),

                       url(r'^500$', 'www.article.views.test500'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
                       # url(r'^admin/', include(admin.site.urls)),
                       )
