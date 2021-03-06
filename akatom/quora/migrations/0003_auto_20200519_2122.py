# Generated by Django 3.0.5 on 2020-05-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0002_auto_20200517_2239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('is_accepted', '-created_at'), 'verbose_name': '答案', 'verbose_name_plural': '答案'},
        ),
        migrations.AddField(
            model_name='question',
            name='clicknum',
            field=models.IntegerField(default=0, verbose_name='浏览量'),
        ),
    ]
