# Generated by Django 2.2.11 on 2020-04-22 13:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muscu_site', '0008_auto_20200401_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsession',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='exercisecompleted',
            name='exercise',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='exercise_completed', to='muscu_site.Exercise'),
        ),
        migrations.AlterField(
            model_name='exercisecompleted',
            name='training_session_completed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_completed', to='muscu_site.TrainingSessionCompleted'),
        ),
        migrations.AlterField(
            model_name='trainingsessioncompleted',
            name='date_completed',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='trainingsessioncompleted',
            name='training_session',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='session_completed', to='muscu_site.TrainingSession'),
        ),
    ]