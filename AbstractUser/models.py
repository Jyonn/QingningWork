from django.db import models


class AbstractUser(models.Model):
    uid = models.AutoField(
        verbose_name="用户编号",
        primary_key=True,
        db_index=True,
        auto_created=True,
        editable=False,
    )
    nickname = models.CharField(
        verbose_name="笔名/称呼",
        max_length=20,
        default=None,
    )
    username = models.CharField(
        verbose_name="用户账号",
        max_length=20,
        default=None,
    )
    password = models.CharField(
        verbose_name="用户密码",
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
    last_ipv4 = models.GenericIPAddressField(
        verbose_name="上次登录IP",
        default=None,
    )
    phone = models.CharField(
        verbose_name="联系方式",
        default=None,
        max_length=20,
    )
    email = models.EmailField(
        verbose_name="电子邮箱",
        default=None,
        max_length=40,
    )
    avatar = models.CharField(
        verbose_name="头像地址",
        default=None,
        max_length=32,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        user = cls(*args, **kwargs)
        user.save()
        return user
