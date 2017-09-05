from django.db import models


class AbstractUser(models.Model):
    WRITER = "writer"
    REVIEWER = "reviewer"
    TYPE_WRITER = 0
    TYPE_REVIEWER = 1
    TYPE_TABLE = (
        (TYPE_WRITER, '作者'),
        (TYPE_REVIEWER, '审稿'),
    )
    L = {
        'nickname': 20,
        'username': 20,
        'password': 40,
        'salt': 8,
        'phone': 20,
        'email': 40,
        'avatar': 32,
        'introduce': 20,
    }
    uid = models.AutoField(
        verbose_name="用户编号",
        primary_key=True,
        db_index=True,
        auto_created=True,
        editable=False,
    )
    user_type = models.IntegerField(
        verbose_name='用户身份',
        default=TYPE_WRITER,
        choices=TYPE_TABLE,
    )
    user_id = models.IntegerField(
        verbose_name='身份表的用户编号',
        default=0,
        null=True,
        blank=True,
    )
    nickname = models.CharField(
        verbose_name="笔名/称呼",
        max_length=L['nickname'],
        default=None,
        unique=True,
        null=True,
    )
    username = models.CharField(
        verbose_name="用户账号",
        max_length=L['username'],
        default=None,
        unique=True,
    )
    password = models.CharField(
        verbose_name="用户密码",
        max_length=L['password'],
        default=None,
        null=True,
    )
    salt = models.CharField(
        verbose_name="加盐哈希",
        max_length=L['salt'],
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
        max_length=L['phone'],
        null=True,
    )
    email = models.EmailField(
        verbose_name="电子邮箱",
        default=None,
        max_length=L['email'],
        null=True,
    )
    avatar = models.CharField(
        verbose_name="头像地址",
        default=None,
        max_length=L['avatar'],
        null=True,
    )
    total_likes = models.IntegerField(
        verbose_name="喜爱总数",
        default=0,
    )
    is_frozen = models.BooleanField(
        verbose_name="是否被冻结",
        default=False,
    )
    introduce = models.CharField(
        verbose_name='一句话介绍',
        max_length=L['introduce'],
        default=None,
        blank=True,
        null=True,
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
        self.save()
        return self

    def get_avatar(self):
        from BaseFunc.cdn import QiNiu
        return QiNiu.host + '/' + self.avatar

    def get_introduce(self):
        return '他还没有填写介绍。' if self.introduce in [None, ''] else self.introduce

    def get_nickname(self):
        return self.username if self.nickname in [None, ''] else self.nickname


class LikeUser(models.Model):
    re_user_liked = models.ForeignKey(
        AbstractUser,
        verbose_name="关联被喜爱用户",
        default=None,
        null=False,
        blank=False,
        related_name="user_liked",
    )
    re_user_to_like = models.ForeignKey(
        AbstractUser,
        verbose_name="关联点评喜爱用户",
        default=None,
        null=False,
        blank=False,
        related_name="user_to_like",
    )
    result = models.NullBooleanField(
        verbose_name="喜爱结果",
        default=None,
        null=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        like_user = cls(*args, **kwargs)
        like_user.save()
        return like_user
