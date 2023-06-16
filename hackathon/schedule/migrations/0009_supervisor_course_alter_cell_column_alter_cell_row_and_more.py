# Generated by Django 4.2.1 on 2023-05-25 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0008_remove_cell_i_remove_cell_j"),
    ]

    operations = [
        migrations.AddField(
            model_name="supervisor",
            name="course",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supervisor",
                to="schedule.coursecode",
            ),
        ),
        migrations.AlterField(
            model_name="cell",
            name="column",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cells",
                to="schedule.column",
            ),
        ),
        migrations.AlterField(
            model_name="cell",
            name="row",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cells",
                to="schedule.row",
            ),
        ),
        migrations.AlterField(
            model_name="column",
            name="time_slot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="columns",
                to="schedule.timeslot",
            ),
        ),
    ]