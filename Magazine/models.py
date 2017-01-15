from django.db import models

from Reviewer.models import Reviewer
from Work.models import Work
from Writer.models import Writer


class Magazine(models.Model):
    title = models.CharField(
        verbose_name="杂志标题",
        max_length=20,
    )
    create_time = models.DateTimeField(
        verbose_name="创建时间",
        default=None,
    )
    intro_writer = models.ForeignKey(
        Writer,
        verbose_name="本期作者",
        default=None,
    )
    intro_words = models.CharField(
        verbose_name="本期作者介绍",
        max_length=300,
        default=None,
    )
    is_public = models.BooleanField(
        verbose_name="是否公开",
        default=False,
    )
    re_reviewer = models.ForeignKey(
        Reviewer,
        verbose_name="关联审稿员",
        default=None,
    )


class MagazineWork(models.Model):
    re_magazine = models.ForeignKey(
        Magazine,
        verbose_name="关联杂志",
        default=None,
    )
    re_work = models.ForeignKey(
        Work,
        verbose_name="关联作品",
        default=None,
    )
    order = models.IntegerField(
        verbose_name="当前杂志的顺序",
        default=0,
    )
