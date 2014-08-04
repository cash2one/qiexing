# -*- coding: utf-8 -*-

import time
import logging
from django.http import Http404
from django.conf import settings
from common import debug, utils


class UserMiddware(object):

    def __init__(self):
        pass

    def process_request(self, request):
        setattr(request, "_process_start_timestamp", time.time())

        sub_domain = utils.get_sub_domain_from_http_host(request.META.get('HTTP_HOST', ''))
        request.sub_domain = sub_domain

    def process_response(self, request, response):
        if hasattr(request, '_process_start_timestamp'):
            t = int((time.time() - float(getattr(request, '_process_start_timestamp'))))
            if t >= 10:
                user_id = request.user.id if request.user.is_authenticated() else "anymouse"
                logging.error("LONG_PROCESS: %s %s %s" % (request.path, t, user_id))
        return response

    def process_exception(self, request, exception):
        if type(exception) == Http404:
            return

        title = u'%s error in %s' % (settings.SERVER_NAME, request.get_full_path())
        content = debug.get_debug_detail(exception)
        if settings.SERVER_NAME != 'DEVELOPER':
            utils.send_email(settings.NOTIFICATION_EMAIL, title, content)
