# Generated by Django 4.1.4 on 2022-12-30 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_project_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLog',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='操作编号')),
                ('ip', models.CharField(default='', max_length=50, verbose_name='操作ip')),
                ('date', models.DateField(verbose_name='操作时间')),
                ('cmd', models.CharField(default='', max_length=50, verbose_name='操作类型')),
                ('other', models.CharField(default='', max_length=70, verbose_name='备注')),
            ],
        ),
    ]