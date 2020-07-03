from django.contrib import admin
from akatom.blogs.models import Article,ArticleCategory
from mdeditor.widgets import MDEditorWidget
from django.db import models
# Register your models here.


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['catname','created_at','updated_at']


class ArticleAdmin(admin.ModelAdmin):

    list_display = ['slug', 'title', 'user', 'category', 'status', 'tags', 'created_at']


admin.site.register(ArticleCategory,ArticleCategoryAdmin)


admin.site.register(Article,ArticleAdmin)


