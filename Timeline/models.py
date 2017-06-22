from django.db import models

from AbstractUser.models import AbstractUser
from Work.models import Work
from Writer.models import Writer


class Timeline(models.Model):
    TYPE_CREATE_WORK = 0
    TYPE_MODIFY_WORK = 1
    TYPE_REPOST_WORK = 2
    TYPE_THUMB_WORK = 3
    TYPE_COMMENT_WORK = 4
    TYPE_REVIEW_WORK = 5
    TYPE_CLAIM_WORK = 6
    TYPE_TABLE = (
        (TYPE_CREATE_WORK, '发表'),
        (TYPE_MODIFY_WORK, '修订'),
        (TYPE_REPOST_WORK, '分享'),
        (TYPE_THUMB_WORK, '点赞'),
        (TYPE_COMMENT_WORK, '评论'),
        (TYPE_REVIEW_WORK, '审核'),
        (TYPE_CLAIM_WORK, '认领'),
    )
    L = {
        'motion': 500,
    }
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_created=True,
        auto_now=True,
    )
    owner = models.ForeignKey(
        AbstractUser,
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
    motion = models.CharField(
        verbose_name='动态发表心情',
        help_text='创建 修改 分享时才有用',
        default=None,
        null=True,
        blank=True,
        max_length=L['motion'],
    )
    extension_id = models.IntegerField(
        verbose_name='扩展ID',
        help_text='如评论ID有效',
        default=-1,
    )

    @classmethod
    def create(cls, o_user, related_work, tl_type, motion=None, extension_id=-1):
        event = cls(
            related_work=related_work,
            owner_id=o_user.uid,
            type=tl_type,
            motion=motion,
            extension_id=extension_id,
        )
        try:
            event.save()
        except:
            return None
        return event

    @staticmethod
    def get_desc(type_id):
        for item in Timeline.TYPE_TABLE:
            if item[0] == type_id:
                return item[1]
        return 'UNK'
