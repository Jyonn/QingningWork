from django.db import models

from AbstractUser.models import AbstractUser
from Writer.models import Writer
from Reviewer.models import Reviewer


class Work(models.Model):
    # 作品状态
    STATUS_UNDER_WRITE = 0  # 正在创作
    STATUS_UNDER_REVIEW = 1  # 正在审稿
    STATUS_RECEIVED = 2  # 审稿通过，商讨稿费
    STATUS_REFUSED = 3  # 审稿驳回
    STATUS_CONFIRM_FEE = 4  # 确认稿费
    # 作品状态允许的转移路线为：0->1, 1->2, 1->3, 2->4，其他状态不被允许且不可逆
    #
    STATUS_TABLE = (
        (STATUS_UNDER_WRITE, '正在创作'),
        (STATUS_UNDER_REVIEW, '正在审稿'),
        (STATUS_RECEIVED, '审稿通过，商讨稿费'),
        (STATUS_REFUSED, '审稿驳回'),
        (STATUS_CONFIRM_FEE, '确认稿费'),
    )

    # 审稿和作者必有一非空
    re_writer = models.ForeignKey(
        Writer,
        verbose_name='关联作者',
        db_index=True,
        default=None,
        null=True,
    )
    re_reviewer = models.ForeignKey(
        Reviewer,
        verbose_name='关联审稿',
        db_index=True,
        default=None,
        null=True,
    )

    # 作品字段
    writer_name = models.CharField(
        verbose_name='笔名',
        db_index=True,
        max_length=10,
        default=None,
        null=True,
    )
    work_name = models.CharField(
        verbose_name='标题',
        db_index=True,
        max_length=20,
        default=None,
    )
    content = models.TextField(
        verbose_name='文章正文',
        default=None,
    )

    # 作品状态字段
    is_public = models.BooleanField(
        verbose_name='是否公开',
        default=True,
    )
    is_delete = models.BooleanField(
        verbose_name='是否被删除',
        default=False,
    )
    status = models.SmallIntegerField(
        verbose_name='作品状态',
        default=STATUS_UNDER_WRITE,
        choices=STATUS_TABLE,
    )
    fee = models.FloatField(
        verbose_name='作品稿费',
        default=0,
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now=True,
        auto_created=True,
    )
    last_version_work = models.ForeignKey(
        'self',
        verbose_name='上一版本的作品',
        default=None,
        null=True,
        blank=True,
        related_name='last_version',
    )
    newest_version_work = models.ForeignKey(
        'self',
        verbose_name='最新版本',
        default=None,
        null=True,
        blank=True,
        related_name='newest_version',
    )
    version_num = models.IntegerField(
        verbose_name='作品第几版',
        default=1,
    )
    is_updated = models.BooleanField(
        verbose_name="是否有更新（此条无效）",
        default=False,
    )
    total_visit = models.IntegerField(
        verbose_name='阅读人数',
        default=0,
    )

    work_group_id = models.IntegerField(
        verbose_name='稿件组',
        default=None,
        null=True,
        blank=True,
    )

    @classmethod
    def create(cls, o_user, work_name, writer_name, content, is_public, one_work):
        try:
            if one_work is None:
                o_work_group = None
                o_latest_work = None
            else:
                o_work_group = WorkGroup.objects.get(pk=one_work.work_group_id)
                o_latest_work = Work.objects.get(pk=o_work_group.latest)
                o_latest_work.is_updated = True
                o_latest_work.save()
        except:
            return None
        re_writer, re_reviewer = None, None
        if o_user.user_type == AbstractUser.TYPE_REVIEWER:
            re_reviewer = o_user
        if o_user.user_type == AbstractUser.TYPE_WRITER:
            re_writer = o_user
        o_work = cls(
            re_writer=re_writer,
            re_reviewer=re_reviewer,
            work_name=work_name,
            writer_name=writer_name,
            content=content,
            is_public=is_public,
            # last_version_work=last_version_work,
            version_num=1 if one_work is None else o_latest_work.version_num + 1,
            is_updated=False,
            status=Work.STATUS_UNDER_REVIEW if is_public else Work.STATUS_UNDER_WRITE,
            work_group_id=None if o_work_group is None else o_work_group.pk,
        )
        try:
            o_work.save()
            if o_work_group is None:
                o_work_group = WorkGroup.create(o_work)
                o_work.work_group_id = o_work_group.pk
                o_work.save()
            else:
                o_work_group.latest = o_work
                o_work_group.save()
        except:
            return None
        return o_work


class WorkGroup(models.Model):
    """
    文章组，多次修改稿件的为一组
    """
    latest = models.ForeignKey(
        Work,
        verbose_name='最新稿',
        unique=True,
    )

    @classmethod
    def create(cls, latest):
        o_work_group = cls(latest=latest)
        try:
            o_work_group.save()
        except:
            return None
        return o_work_group
