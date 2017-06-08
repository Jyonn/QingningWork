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
    owner = models.ForeignKey(
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
    is_delete = models.BooleanField(
        verbose_name='是否删除',
        default=False,
    )

    @classmethod
    def create(cls, related_writer, related_work, tl_type, **kwargs):
        event = cls(
            related_work=related_work,
            related_writer=related_writer,
            type=tl_type,
            **kwargs,
        )
        event.save()
        return event
