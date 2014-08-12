# -*- coding: utf-8 -*-

import json

from common import utils, cache, debug
from www.misc.decorators import cache_required
from www.misc import consts
from www.message.models import UnreadCount, UnreadType, Notice,  GlobalNotice


dict_err = {
    60100: u'自己不能邀请自己哦',
    60101: u'最多邀请6人',
    60102: u'已邀请，请勿重复邀请',
    60103: u'没有找到对应的通知'
}
dict_err.update(consts.G_DICT_ERROR)

DEFAULT_DB = 'default'


class UnreadCountBase(object):

    """
    @note: 封装未读数信息操作类
    """

    def __init__(self):
        self.cache_obj = cache.Cache(config=cache.CACHE_TMP)

    def __del__(self):
        del self.cache_obj

    @cache_required(cache_key='unread_type_all', expire=0, cache_config=cache.CACHE_STATIC)
    def get_unread_type(self, must_update_cache=False):
        """
        @note: 获取提醒类型数据
        """
        return UnreadType.objects.all().order_by('type', 'id')

    def get_or_create_count_info(self, user):
        """
        @note: 获取用户未读数对象
        """
        user_id = utils.get_uid(user)
        obj_urcs = UnreadCount.objects.filter(user_id=user_id)
        created = True
        if not obj_urcs:
            count_info = self.init_count_info()
            urc = UnreadCount.objects.create(user_id=user_id, count_info=json.dumps(count_info))
            created = False
        else:
            urc = obj_urcs[0]
        return urc, created

    def init_count_info(self):
        """
        @note: 获取初始未读数信息
        """

        nts = self.get_unread_type()
        count_info = {}
        for nt in nts:
            count_info.setdefault(str(nt.code), 0)
        return count_info

    def update_unread_count(self, user, code, operate="add"):
        """
        @note: 更新提醒未读数
        """

        if UnreadType.objects.filter(code=code).count() == 0:
            return False

        urc, created = self.get_or_create_count_info(user)
        count_info = json.loads(urc.count_info)

        if not count_info.has_key(code):
            count_info.setdefault(code, 0)
        # 加一或者重置
        if operate == 'add':
            count_info[code] += 1
        else:
            count_info[code] = 0

        urc.count_info = json.dumps(count_info)
        urc.save()
        # 操作缓存
        user_id = utils.get_uid(user)
        cache_key = u'%s_%s' % ('unread_count', user_id)
        self.cache_obj.set(cache_key, count_info, 3600 * 24)

        return True

    @cache_required(cache_key='unread_count_%s', expire=3600 * 24)
    def get_unread_count_info(self, user):
        """
        @note: 获取未读数
        """
        user_id = utils.get_uid(user)
        try:
            count_info = json.loads(UnreadCount.objects.get(user_id=user_id).count_info)
        except UnreadCount.DoesNotExist:
            count_info = self.init_count_info()  # 没有就不用自动创建，更新的时候进行创建
        return count_info

    def get_unread_count_total(self, user):
        count_info = self.get_unread_count_info(user)
        return count_info

    def clear_count_info_by_code(self, user_id, code):
        """
        @note: 通用的清除消息数的方法，数字大于0的才去调用清除，提高效率
        """
        if code and user_id and int(UnreadCountBase().get_unread_count_info(user_id).get(code, 0)) > 0:
            UnreadCountBase().update_unread_count(user_id, code, operate='clear')

    def get_system_message(self, user_id):
        return Notice.objects.filter(user_id=user_id)

    def add_system_message(self, user_id, content, source=0):
        notice = Notice.objects.create(user_id=user_id, content=content, source=source)
        UnreadCountBase().update_unread_count(user_id, code='system_message')
        return notice


class GlobalNoticeBase(object):

    def __init__(self):
        pass

    def format_global_notice(self, objs):
        data = []
        for obj in objs:
            data.append(dict(notice_id=obj.id, content=obj.content, level=obj.level))
        return data

    def create_global_notice(self, content, start_time, end_time, user_id, level=0, platform=0):
        try:
            assert content and start_time and end_time
            assert end_time > start_time
        except:
            return 99800, dict_err.get(99800)

        obj = GlobalNotice.objects.create(content=content, start_time=start_time, end_time=end_time,
                                          user_id=user_id, level=level, platform=platform)

        self.get_all_valid_global_notice(must_update_cache=True)
        return 0, obj.id

    @cache_required(cache_key='get_all_valid_global_notice', expire=3600)
    def get_all_valid_global_notice(self, must_update_cache=False):
        import datetime
        now = datetime.datetime.now()
        return GlobalNotice.objects.filter(end_time__gt=now, start_time__lt=now)

    def get_all_global_notice(self):
        return GlobalNotice.objects.all()

    def get_notice_by_id(self, notice_id):
        if not notice_id:
            return None

        obj = GlobalNotice.objects.filter(id=notice_id)
        if not obj:
            return None

        return obj[0]

    def modify_global_notice(self, notice_id, **kwargs):
        try:
            assert kwargs.get('content') and kwargs.get('start_time') and kwargs.get('end_time')
            assert kwargs.get('end_time') > kwargs.get('start_time')
        except:
            return 99800, dict_err.get(99800)

        if not notice_id:
            return 60103, dict_err.get(60103)

        obj = GlobalNotice.objects.filter(id=notice_id)
        if not obj:
            return 60103, dict_err.get(60103)

        obj = obj[0]
        try:
            for k, v in kwargs.items():
                setattr(obj, k, v)

            obj.save()
        except Exception, e:
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)

        # 更新缓存
        self.get_all_valid_global_notice(must_update_cache=True)
        return 0, dict_err.get(0)

    def remove_global_notice(self, notice_id):
        if not notice_id:
            return 60103, dict_err.get(60103)

        obj = GlobalNotice.objects.filter(id=notice_id)
        if not obj:
            return 60103, dict_err.get(60103)

        obj.delete()

        # 更新缓存
        self.get_all_valid_global_notice(must_update_cache=True)
        return 0, dict_err.get(0)
