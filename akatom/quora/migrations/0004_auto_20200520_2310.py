# Generated by Django 3.0.5 on 2020-05-20 15:10

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0003_auto_20200519_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=markdownx.models.MarkdownxField(verbose_name='问题内容'),
        ),
    ]
