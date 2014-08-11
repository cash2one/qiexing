# -*- coding: utf-8 -*-

from django.db import models
# from django.conf import settings


class Sight(models.Model):
    province_key = models.CharField(max_length=32, db_index=True)
    name = models.CharField(max_length=32, unique=True)
    des = models.TextField()
    code = models.CharField(max_length=32, unique=True)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ["-id", ]

    def get_url(self):
        return u'/sight/%s' % self.id


class SightImg(models.Model):
    sight = models.ForeignKey(Sight)
    img = models.CharField(max_length=256)

    class Meta:
        ordering = ["-id", ]
