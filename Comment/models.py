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
        verbose_name='评论（v2）',
        max_length=500,
        default=None,
        blank=True,
        null=True,
    )
    result = models.BooleanField(
        verbose_name="审稿结果",
        default=RESULT_RECEIVE,
    )
    comment_time = models.DateTimeField(
        verbose_name="审稿时间",
        auto_created=True,
        auto_now=True,
    )
    is_updated = models.BooleanField(
        verbose_name="是否有更新（此条无效）",
        default=False,
    )

    @classmethod
    def create(cls, re_work, re_reviewer, content, result):
        comment = cls(
            re_work=re_work,
            re_reviewer=re_reviewer,
            content=content,
            result=result,
        )
        comment.save()
        return comment

    def get_html_id(self):
        return 'comment-r'+str(self.pk)


class WriterComment(models.Model):
    L = {
        'content': 500,
    }
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
        max_length=L['content'],
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
    def create(cls, re_work, re_writer, content):
        w_comment = cls(
            re_work=re_work,
            re_writer=re_writer,
            content=content,
        )
        w_comment.save()
        return w_comment

    def get_html_id(self):
        return 'comment-w'+str(self.pk)


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
    def create(cls, re_work, re_writer, is_deleted):
        w_like = cls(
            re_work=re_work,
            re_writer=re_writer,
            is_deleted=is_deleted,
        )
        w_like.save()
        return w_like
