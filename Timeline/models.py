from django.db import models

from Work.models import Work
from Writer.models import Writer


class Timeline(models.Model):
    TYPE_CREATE_WORK = 0
    TYPE_MODIFY_WORK = 1
    TYPE_REPOST_WORK = 2
    TYPE_THUMB_WORK = 3
    TYPE_COMMENT_WORK = 4
    TYPE_TABLE = (
        (TYPE_CREATE_WORK, '创建作品'),
        (TYPE_MODIFY_WORK, '修改作品'),
        (TYPE_REPOST_WORK, '分享作品'),
        (TYPE_THUMB_WORK, '点赞作品'),
        (TYPE_COMMENT_WORK, '评论作品'),
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_created=True,
        auto_now=True,
    )
    related_writer = models.ForeignKey(
        Writer,
        verbose_name='所属用户',
        db_index=True,
    )
    related_work = models.ForeignKey(
        Work,
        verbose_name='关联作品',
        db_index=True,
    )
    type = models.IntegerField(
        verbose_name='时间线内容类型',
        choices=TYPE_TABLE,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        event = cls(*args, **kwargs)
        event.save()
        return event
