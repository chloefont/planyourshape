from django.contrib import admin
from muscu_site.models import TrainingSession, Exercice

class ExerciceInLine(admin.TabularInline):
    model = Exercice

class TrainingSessionAdmin(admin.ModelAdmin):
    inlines = [ExerciceInLine]

admin.site.register(TrainingSession, TrainingSessionAdmin)
