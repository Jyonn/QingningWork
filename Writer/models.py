# coding=utf-8
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
    total_follow = models.IntegerField(
        verbose_name='我的关注',
        default=0,
    )
    total_followed = models.IntegerField(
        verbose_name='我的粉丝',
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
        avatar_int = randint(1, 10)
        avatar_img = "0" if avatar_int < 10 else ""
        avatar_img += str(avatar_int)
        writer.avatar = "img/avatar/default-" + avatar_img + ".jpg"
        writer.save()
        return writer


class Follow(models.Model):
    followee = models.ForeignKey(
        Writer,
        verbose_name='关注者',
        related_name='followee',
    )
    follower = models.ForeignKey(
        Writer,
        verbose_name='追随者',
        related_name='follower',
    )
    create_time = models.DateTimeField(
        auto_now=True,
        auto_created=True,
    )
    is_delete = models.BooleanField(
        verbose_name='是否删除（取消关注）',
        default=False,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        follow = cls(*args, **kwargs)
        follow.save()
        return follow
