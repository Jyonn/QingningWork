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
    STATUS_TABLE = [
        (STATUS_UNDER_WRITE, "正在创作"),
        (STATUS_UNDER_REVIEW, "正在审稿"),
        (STATUS_RECEIVED, "审稿通过，商讨稿费"),
        (STATUS_REFUSED, "审稿驳回"),
        (STATUS_CONFIRM_FEE, "确认稿费"),
    ]

    # 作品类型
    WORK_TYPE_TEXT = 0
    WORK_TYPE_FILE = 1

    # 审稿和作者必有一非空
    re_writer = models.ForeignKey(
        Writer,
        verbose_name="关联作者",
        default=None,
        null=True,
    )
    re_reviewer = models.ForeignKey(
        Reviewer,
        verbose_name="关联审稿",
        default=None,
        null=True,
    )

    # 作品字段
    writer_name = models.CharField(
        verbose_name="笔名",
        max_length=10,
        default=None,
        null=True,
    )
    work_name = models.CharField(
        verbose_name="标题",
        max_length=20,
        default=None,
    )
    work_store = models.CharField(
        verbose_name="存储路径",
        max_length=32,
        default=None,
    )
    work_type = models.SmallIntegerField(
        verbose_name="作品类型",
        default=WORK_TYPE_TEXT,
    )

    # 作品状态字段
    is_public = models.BooleanField(
        verbose_name="是否公开",
        default=True,
    )
    is_delete = models.BooleanField(
        verbose_name="是否被删除",
        default=False,
    )
    status = models.SmallIntegerField(
        verbose_name="作品状态",
        default=STATUS_UNDER_WRITE,
    )
    fee = models.FloatField(
        verbose_name="作品稿费",
        default=0,
    )
    create_time = models.DateTimeField(
        verbose_name="创建时间",
        default=None,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        work = cls(*args, **kwargs)
        work.save()
        return work

