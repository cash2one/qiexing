# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('www.answer.views',
                       url(r'^create_answer$', 'create_answer'),
                       url(r'^modify_answer$', 'modify_answer'),
                       url(r'^remove_answer$', 'remove_answer'),
                       )
