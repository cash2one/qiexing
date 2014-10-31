# -*- coding: utf-8 -*-

"""
@attention: 定义全局上下文变量
@author: lizheng
@date: 2011-11-28
"""


def config(request):
    """
    @attention: Adds settings-related context variables to the context.
    """
    import datetime
    from django.conf import settings
    from www.admin.interface import StaticPageBase

    return {
        'DEBUG': settings.DEBUG,
        'LOCAL_FLAG': settings.LOCAL_FLAG,
        'MEDIA_VERSION': '005',
        'SERVER_DOMAIN': settings.SERVER_DOMAIN,
        'MAIN_DOMAIN': settings.MAIN_DOMAIN,
        'IMG0_DOMAIN': settings.IMG0_DOMAIN,
        "YEAR": datetime.datetime.now().strftime("%Y"),
        "STATIC_PAGE_CONTENT": StaticPageBase().get_static_page(),
    }
