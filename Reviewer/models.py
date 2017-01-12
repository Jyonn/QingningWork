from django.db import models
from AbstractUser.models import AbstractUser


class Reviewer(AbstractUser):
    rid = models.AutoField(
        "审稿员编号",
        primary_key=True,
        db_index=True,
        auto_created=True,
        editable=False,
    )
    total_review = models.IntegerField(
        verbose_name="审稿总数",
        default=0,
    )
    total_received = models.IntegerField(
        verbose_name="审阅通过作品",
        default=0,
    )
    total_refused = models.IntegerField(
        verbose_name="审阅驳回作品",
        default=0,
    )
    total_upload = models.IntegerField(
        verbose_name="传稿总数",
        default=0,
    )
    privilege = models.SmallIntegerField(
        verbose_name="特权等级",
        default=0,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        reviewer = cls(*args, **kwargs)
        reviewer.save()
        return reviewer

