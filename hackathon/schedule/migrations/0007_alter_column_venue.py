# Generated by Django 4.2.1 on 2023-05-22 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0006_alter_column_venue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="column",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="column",
                to="schedule.venue",
            ),
        ),
    ]
