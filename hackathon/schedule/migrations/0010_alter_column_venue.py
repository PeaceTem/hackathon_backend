# Generated by Django 4.2.1 on 2023-05-25 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "schedule",
            "0009_supervisor_course_alter_cell_column_alter_cell_row_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="column",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="columns",
                to="schedule.venue",
            ),
        ),
    ]
