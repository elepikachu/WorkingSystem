# Generated by Django 4.1 on 2023-01-11 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyitem", "0004_item_classif"),
    ]

    operations = [
        migrations.CreateModel(
            name="Suggestion",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="建议编号"
                    ),
                ),
                (
                    "ip",
                    models.CharField(default="", max_length=50, verbose_name="操作ip"),
                ),
                ("date", models.DateTimeField(verbose_name="提出时间")),
                (
                    "type",
                    models.CharField(default="", max_length=30, verbose_name="建议类型"),
                ),
                (
                    "detail",
                    models.CharField(default="", max_length=500, verbose_name="建议"),
                ),
            ],
        ),
    ]
