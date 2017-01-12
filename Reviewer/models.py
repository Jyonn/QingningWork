from django.db import models


class Reviewer(models.Model):
    rid = models.AutoField(
        "审稿员编号",
        primary_key=True,
        db_index=True,
        auto_created=True,
        editable=False,
    )
    username = models.CharField(
        verbose_name="审稿员",
        max_length=20,
        default=None,
    )
    password = models.CharField(
        verbose_name="审稿员密码",
        max_length=40,
        default=None,
        blank=True,
    )
    pwd_login = models.BooleanField(
        verbose_name="是否需要密码登录",
        default=True,
    )
    last_login = models.DateTimeField(
        verbose_name="上次登录时间",
        default=None,
    )
    last_ipv4 = models.IPAddressField(
        verbose_name="上次登录IP",
        default=None,
    )
    total_review = models.IntegerField(
        verbose_name="审稿总数",
        default=0,
    )
    total_upload = models.IntegerField(
        verbose_name="传稿总数",
        default=0,
    )
    phone = models.CharField(
        verbose_name="联系方式",
        default=None,
        max_length=20,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        reviewer = cls(*args, **kwargs)
        reviewer.save()
        return reviewer
