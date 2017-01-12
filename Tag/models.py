from django.db import models


class Tag(models.Model):
    attr = models.CharField(
        verbose_name="标签内容",
        max_length=10,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        tag = cls(*args, **kwargs)
        tag.save()
        return tag
