# -*- coding: utf-8 -*-

from django.db import models


class Answer(models.Model):
    obj_type_choices = ((0, u"游记"), (1, u"活动"), (2, u"装备"))

    from_user_id = models.CharField(verbose_name=u'回答者', max_length=32, db_index=True)
    to_user_id = models.CharField(verbose_name=u'被回答者', max_length=32, db_index=True)
    content = models.TextField()
    obj_type = models.IntegerField(db_index=True, choices=obj_type_choices)
    obj_id = models.IntegerField(db_index=True)
    sort_num = models.IntegerField(verbose_name=u'排序值', default=0, db_index=True)
    like_count = models.IntegerField(verbose_name=u'赞的次数', default=0)
    ip = models.CharField(max_length=32, null=True)
    # is_bad = models.BooleanField(default=False)  # 是否是无用回复，无用回复需要折叠
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ["-sort_num", "-like_count", "id"]

    def get_url(self):
        return u'/question/%s#to_answer_%s' % (self.question_id, self.id)

    def get_from_user(self):
        from www.account.interface import UserBase
        return UserBase().get_user_by_id(self.from_user_id)

    def get_to_user(self):
        from www.account.interface import UserBase
        return UserBase().get_user_by_id(self.to_user_id)

    def get_summary(self, max_num=100):
        """
        @attention: 通过内容获取摘要
        """
        from common import utils
        return utils.get_summary_from_html_by_sub(self.content, max_num=max_num)


class AtAnswer(models.Model):
    answer = models.ForeignKey(Answer)
    user_id = models.CharField(max_length=32)

    class Meta:
        unique_together = [('user_id', 'answer')]
        ordering = ["-id"]
