from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import CharField

class User(AbstractUser):
    # id = models.AutoField(primary_key=True)
    # slug = models.SlugField(unique=True)
    nickname = models.CharField(verbose_name='用户昵称', blank=True, null=True, max_length=255, default='')
    job = models.CharField(verbose_name='用户职业', blank=True, null=True, max_length=50,default='未知')
    introduction = models.TextField(blank=True, null=True, verbose_name='简介', default='该用户很懒，啥也没写...')
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='用户头像', default='')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='住址', default='')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True, default=timezone.now)
    personal_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='个人链接', default='')
    weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name='微博链接', default='')
    zhihu = models.URLField(max_length=255, null=True, blank=True, verbose_name='知乎链接', default='')
    github = models.URLField(max_length=255, null=True, blank=True, verbose_name='GitHub链接', default='')
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name='LinkedIn链接', default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
