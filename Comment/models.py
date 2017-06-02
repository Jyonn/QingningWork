from django.db import models
from Work.models import Work
from Reviewer.models import Reviewer
from Writer.models import Writer


class Comment(models.Model):
    # 审稿结果
    RESULT_RECEIVE = True,
    RESULT_REFUSE = False,

    re_work = models.ForeignKey(
        Work,
        verbose_name="关联作品",
        blank=False,
        db_index=True,
    )
    re_reviewer = models.ForeignKey(
        Reviewer,
        verbose_name="关联审稿员",
        blank=False,
        db_index=True,
    )
    content = models.CharField(
        verbose_name="评论",
        max_length=500,
        default=None,
    )
    result = models.BooleanField(
        verbose_name="审稿结果",
        default=RESULT_RECEIVE,
    )
    comment_time = models.DateTimeField(
        verbose_name="审稿时间",
        auto_created=True,
    )
    is_updated = models.BooleanField(
        verbose_name="是否有更新（此条无效）",
        default=False,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        comment = cls(*args, **kwargs)
        comment.save()
        return comment


class WriterComment(models.Model):
    re_work = models.ForeignKey(
        Work,
        verbose_name="关联作品",
        blank=False,
        db_index=True,
    )
    re_writer = models.ForeignKey(
        Writer,
        verbose_name="关联作者",
        blank=False,
        db_index=True,
    )
    content = models.CharField(
        verbose_name="评论",
        max_length=500,
        default=None,
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now=True,
        auto_created=True,
    )
    is_deleted = models.BooleanField(
        verbose_name="是否被删除",
        default=False,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        w_comment = cls(*args, **kwargs)
        w_comment.save()
        return w_comment


class WriterLike(models.Model):
    re_work = models.ForeignKey(
        Work,
        verbose_name="关联作品",
        blank=False,
        db_index=True,
    )
    re_writer = models.ForeignKey(
        Writer,
        verbose_name="关联作者",
        blank=False,
        db_index=True,
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now=True,
        auto_created=True,
    )
    is_deleted = models.BooleanField(
        verbose_name="是否被删除",
        default=False,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        w_like = cls(*args, **kwargs)
        w_like.save()
        return w_like
