from django.db import models
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
        default=None,
        null=True,
    )
    re_reviewer = models.ForeignKey(
        Reviewer,
        verbose_name='关联审稿',
        default=None,
        null=True,
    )

    # 作品字段
    writer_name = models.CharField(
        verbose_name='笔名',
        max_length=10,
        default=None,
        null=True,
    )
    work_name = models.CharField(
        verbose_name='标题',
        max_length=20,
        default=None,
    )
    work_store = models.CharField(
        verbose_name='存储路径',
        max_length=32,
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

    @classmethod
    def create(cls, *args, **kwargs):
        work = cls(*args, **kwargs)
        work.save()
        return work
