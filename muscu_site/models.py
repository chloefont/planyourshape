import datetime
from django.db import models
from django.contrib.auth.models import User


class TrainingSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="training_session", null=True
    )
    session_title = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    visible = models.BooleanField(default=True)

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

    def __str__(self):
        return self.exercise


class TrainingSessionCompleted(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="training_session_completed", null=True
    )
    training_session = models.ForeignKey(
        TrainingSession, on_delete=models.PROTECT, related_name='sessions_completed'
    )
    date_completed = models.DateField(default=datetime.date.today)


class ExerciseCompleted(models.Model):
    training_session_completed = models.ForeignKey(
        TrainingSessionCompleted, on_delete=models.CASCADE, related_name='exercises_completed'
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.PROTECT, related_name='exercises_completed'
    )
    weight = models.PositiveIntegerField(default=0, blank=True)
    comment = models.TextField(blank=True)
