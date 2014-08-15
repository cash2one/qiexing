# -*- coding: utf-8 -*-

from django.db import models


class Permission(models.Model):

    '''
    权限类 
    '''
    name = models.CharField(verbose_name=u'权限名称', max_length=64, unique=True)
    code = models.CharField(verbose_name=u'权限代码', max_length=32, unique=True)
    parent = models.ForeignKey('self', verbose_name=u'父权限', related_name="children", null=True)

    def __unicode__(self):
        return '%s-%s' % (self.name, self.code)


class UserPermission(models.Model):

    '''
    用户权限表
    '''
    user_id = models.CharField(verbose_name=u'用户', max_length=32, db_index=True)
    permission = models.ForeignKey(Permission, verbose_name=u'权限')
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    creator = models.CharField(verbose_name=u'创建者', max_length=32)

    class Meta:
        unique_together = [('user_id', 'permission')]


class FriendlyLink(models.Model):
    link_type_choices = ((0, u'开户子站单个城市的链接'), (1, u'开户子站home页链接'), (2, u'主站内页链接'), (3, u'主站首页链接'))

    name = models.CharField(max_length=32)
    href = models.CharField(max_length=128)
    city_id = models.IntegerField(verbose_name=u'城市信息', db_index=True, null=True)
    img = models.CharField(max_length=64, null=True)
    des = models.CharField(max_length=128, null=True)
    link_type = models.IntegerField(default=0, choices=link_type_choices)
    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = [("name", "city_id", 'link_type'), ]
        ordering = ["-sort_num", "id"]
