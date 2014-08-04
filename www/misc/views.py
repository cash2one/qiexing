# -*- coding: utf-8 -*-

import os
from django.http import HttpResponse, Http404
from django.conf import settings


def txt_view(request, txt_file_name):
    '''
    @note: txt文件展示，主要是提供给搜索引擎
    '''
    file_name = os.path.abspath(os.path.join(settings.SITE_ROOT, '../static/txt/%s.txt' % txt_file_name))
    if not os.path.exists(file_name):
        raise Http404
    return HttpResponse(open(file_name))
