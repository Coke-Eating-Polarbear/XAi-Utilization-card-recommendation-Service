# Generated by Django 5.1 on 2024-08-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("card_recommendation", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="image_url",
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name="card",
            name="link",
            field=models.URLField(),
        ),
    ]