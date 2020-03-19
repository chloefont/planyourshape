from django.contrib import admin
from muscu_site.models import TrainingSession, Exercise

class ExerciseInLine(admin.TabularInline):
    model = Exercise

class TrainingSessionAdmin(admin.ModelAdmin):
    inlines = [ExerciseInLine]

admin.site.register(TrainingSession, TrainingSessionAdmin)
