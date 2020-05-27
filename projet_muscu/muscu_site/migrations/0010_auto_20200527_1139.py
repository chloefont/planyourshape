# Generated by Django 2.2.11 on 2020-05-27 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muscu_site', '0009_auto_20200422_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisecompleted',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='exercisecompleted',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exercises_completed', to='muscu_site.Exercise'),
        ),
        migrations.AlterField(
            model_name='exercisecompleted',
            name='training_session_completed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises_completed', to='muscu_site.TrainingSessionCompleted'),
        ),
        migrations.AlterField(
            model_name='exercisecompleted',
            name='weight',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='trainingsessioncompleted',
            name='training_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sessions_completed', to='muscu_site.TrainingSession'),
        ),
    ]
