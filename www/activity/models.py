# -*- coding: utf-8 -*-

import datetime
from django.db import models


class Activity(models.Model):
    user_id = models.CharField(max_length=32, db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    sign_up_end_date = models.DateField()  # 报名截止时间
    activity_cover = models.CharField(max_length=128)  # 封面
    addr = models.CharField(max_length=64)
    assembly_point = models.CharField(max_length=64)  # 集合地点
    title = models.CharField(max_length=128)
    content = models.TextField()

    answer_count = models.IntegerField(default=0)
    last_answer_time = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    person_count = models.IntegerField(default=0)
    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ["-sort_num", '-start_date']

    def get_url(self):
        return u'/activity/%s' % self.id

    def get_summary(self):
        """
        @attention: 通过内容获取摘要
        """
        from common import utils
        return utils.get_summary_from_html_by_sub(self.content)

    def get_user(self):
        from www.account.interface import UserBase
        return UserBase().get_user_by_id(self.user_id)


class ActivityPerson(models.Model):
    activity = models.ForeignKey(Activity)
    user_id = models.CharField(max_length=32, db_index=True)
    real_name = models.CharField(max_length=16)
    mobile = models.CharField(max_length=16)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        unique_together = [('activity', 'user_id')]
        ordering = ['-id']
