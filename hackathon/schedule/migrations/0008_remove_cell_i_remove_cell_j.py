# Generated by Django 4.2.1 on 2023-05-24 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0007_alter_column_venue"),
    ]

    operations = [
        migrations.RemoveField(model_name="cell", name="i",),
        migrations.RemoveField(model_name="cell", name="j",),
    ]
