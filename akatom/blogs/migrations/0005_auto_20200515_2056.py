# Generated by Django 3.0.5 on 2020-05-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20200506_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, verbose_name='文章标题'),
        ),
    ]
