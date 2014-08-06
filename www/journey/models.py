# -*- coding: utf-8 -*-

from django.db import models


class Journey(models.Model):

    """
    @note: 游记
    """
    user_id = models.CharField(max_length=32, db_index=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    views_count = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    last_answer_time = models.DateTimeField(db_index=True)
    sort_num = models.IntegerField(default=0, db_index=True)
    like_count = models.IntegerField(default=0)
    is_important = models.BooleanField(default=False)   # 是否是精华帖
    is_silence = models.BooleanField(default=False, db_index=True)   # 是否静默，部分话题下的提问采取静默模式，不发feed，不在全部信息中展示
    ip = models.CharField(max_length=32, null=True)
    is_hide_user = models.BooleanField(default=False)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ["-sort_num", '-like_count', "-last_answer_time"]

    def get_url(self):
        return u'/journey/%s' % self.id

    def get_summary(self):
        """
        @attention: 通过内容获取摘要
        """
        from common import utils
        return utils.get_summary_from_html_by_sub(self.content)

    def get_user(self):
        from www.account.interface import UserBase
        return UserBase().get_user_by_id(self.user_id)


class Like(models.Model):

    """
    @note: 喜欢
    """
    journey = models.ForeignKey(Journey)
    from_user_id = models.CharField(verbose_name=u'发起赞的人', max_length=32, db_index=True)
    to_user_id = models.CharField(verbose_name=u'被赞者', max_length=32, db_index=True)
    ip = models.IPAddressField(db_index=True)
    is_anonymous = models.BooleanField(verbose_name=u'是否匿名', db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id', ]

    def __unicode__(self):
        return '%s, %s' % (self.from_user_id, self.to_user_id)
