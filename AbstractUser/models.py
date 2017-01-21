from django.db import models


class AbstractUser(models.Model):
    WRITER = "writer"
    REVIEWER = "reviewer"
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
        unique=True,
        null=True,
    )
    username = models.CharField(
        verbose_name="用户账号",
        max_length=20,
        default=None,
        unique=True,
    )
    password = models.CharField(
        verbose_name="用户密码",
        max_length=40,
        default=None,
        null=True,
    )
    salt = models.CharField(
        verbose_name="加盐哈希",
        max_length=8,
        default=None,
        null=True,
    )
    pwd_login = models.BooleanField(
        verbose_name="是否需要密码登录",
        default=True,
    )
    last_login = models.DateTimeField(
        verbose_name="上次登录时间",
        default=None,
        null=True,
    )
    last_ipv4 = models.GenericIPAddressField(
        verbose_name="上次登录IP",
        default=None,
        null=True,
    )
    this_login = models.DateTimeField(
        verbose_name="本次登录时间",
        default=None,
        null=True,
    )
    this_ipv4 = models.GenericIPAddressField(
        verbose_name="本次登录IP",
        default=None,
        null=True,
    )
    login_times = models.IntegerField(
        verbose_name="登录次数",
        default=0,
    )
    phone = models.CharField(
        verbose_name="联系方式",
        default=None,
        max_length=20,
        null=True,
    )
    email = models.EmailField(
        verbose_name="电子邮箱",
        default=None,
        max_length=40,
        null=True,
    )
    avatar = models.CharField(
        verbose_name="头像地址",
        default=None,
        max_length=32,
        null=True,
    )
    is_frozen = models.BooleanField(
        verbose_name="是否被冻结",
        default=False,
    )

    @staticmethod
    def sha_text(salted_raw_password):
        import hashlib
        sha = hashlib.sha1()
        sha.update(salted_raw_password.encode())
        return sha.hexdigest()

    @staticmethod
    def get_encrypt_password(raw_password):
        from django.utils.crypto import get_random_string
        salt = get_random_string(length=8)
        return salt, AbstractUser.sha_text(salt + raw_password)

    def check_password(self, raw_password):
        encrypted = AbstractUser.sha_text(self.salt + raw_password)
        return encrypted == self.password

    def set_password(self, raw_password):
        salt, encrypted = AbstractUser.get_encrypt_password(raw_password)
        self.salt = salt
        self.password = encrypted
        return self
