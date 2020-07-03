import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
# Create your models here.

User = get_user_model()


class News(models.Model):

    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL, related_name='publishes',
                             verbose_name='用户')
    content = models.TextField(verbose_name='新闻内容')
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="liked_news",
                                    verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE,
                               related_name='children', verbose_name='父级自关联')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at", "-created_at")

    def __str__(self):
        return self.content

    def switch_like(self, user):
        """点赞或者取消点赞"""
        if user in self.likers.all():
            self.likers.remove(user)
            """#如果用户点过赞，再点一次就是取消"""
        else:
            self.likers.add(user)  # 如果用户没点赞，就加入到点赞列表中

    def get_parent(self):
        """永远返回的是新闻"""
        if self.parent:
            return self.parent
        else:
            return self

    def get_children(self):
        """获取当前记录的所有子记录"""
        parent = self.get_parent()
        return parent.children.all()

    def reply_this(self, user, text):
        """
        回复首页的动态
        :param user:登录的用户
        :param text: 回复的内容
        :return: None
        """
        parent = self.get_parent()
        News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )

    def likers_count(self):
        """获取点赞数"""
        return self.likers.count()

    def get_likers(self):
        """所有点赞用户"""
        return self.likers.all()

    def replies_count(self):
        """评论数量"""
        return self.get_children().count()
