# Generated by Django 4.1 on 2023-01-09 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0005_alter_projectlog_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="finish",
            field=models.IntegerField(default=0, verbose_name="是否完成"),
        ),
    ]