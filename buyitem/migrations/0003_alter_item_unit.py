# Generated by Django 4.1 on 2023-01-09 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyitem", "0002_alter_item_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="unit",
            field=models.CharField(default=0, max_length=5, verbose_name="单位"),
        ),
    ]
