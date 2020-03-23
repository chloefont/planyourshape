import datetime

from django.db import models


class TrainingSession(models.Model):
    session_title = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    date_completed = models.DateField(null=True)

    def __str__(self):
        return self.session_title


class Exercise(models.Model):
    training_session = models.ForeignKey(
        TrainingSession, on_delete=models.CASCADE, related_name='exercises'
    )
    exercise = models.CharField(max_length=100, blank=True)
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(default=1)
    break_time = models.PositiveIntegerField(default=60)
    weight = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=500, blank=True)
