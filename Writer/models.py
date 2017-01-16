from django.db import models
from AbstractUser.models import AbstractUser


class Writer(AbstractUser):
    wid = models.AutoField(
        verbose_name="作家编号",
        primary_key=True,
        db_index=True,
        auto_created=True,
        editable=False,
    )
    total_works = models.IntegerField(
        verbose_name="全部作品数",
        default=0,
    )
    total_received = models.IntegerField(
        verbose_name="被接纳的投稿作品数",
        default=0,
    )
    total_refused = models.IntegerField(
        verbose_name="被驳回的投稿作品数",
        default=0,
    )
    total_fee = models.FloatField(
        verbose_name="全部稿费",
        default=0,
    )
    remain_fee = models.FloatField(
        verbose_name="剩余稿费",
        default=0,
    )
    fee_method = models.CharField(
        verbose_name="文字描述获取稿费的方式",
        default=None,
        max_length=50,
        null=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        writer = cls(*args, **kwargs)
        from random import randint
        avatar_int = randint(0, 10)
        avatar_img = "0" if avatar_int < 10 else ""
        avatar_img += str(avatar_int)
        writer.avatar = "default-avatar-" + avatar_img + ".jpg"
        writer.save()
        return writer
