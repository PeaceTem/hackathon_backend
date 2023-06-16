# Generated by Django 4.2.1 on 2023-06-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("object", "0002_institution"),
    ]

    operations = [
        migrations.AddField(
            model_name="object",
            name="object_type",
            field=models.CharField(
                choices=[("key", "key"), ("value", "value")],
                default="value",
                max_length=15,
            ),
            preserve_default=False,
        ),
    ]
