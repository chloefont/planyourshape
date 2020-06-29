# Generated by Django 2.2.10 on 2020-03-02 08:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('sets', models.IntegerField(default=1)),
                ('reps', models.IntegerField(default=1)),
                ('break_time', models.IntegerField(default=60)),
                ('training_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercice', to='muscu_site.TrainingSession')),
            ],
        ),
    ]