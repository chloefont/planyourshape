from django.contrib import admin
from django.utils.safestring import mark_safe
from muscu_site.models import TrainingSession, Exercise, TrainingSessionCompleted, ExerciseCompleted


class ExerciseInLine(admin.TabularInline):
    model = Exercise


class TrainingSessionAdmin(admin.ModelAdmin):
    inlines = [ExerciseInLine]


class ExerciseCompletedInLine(admin.TabularInline):
    model = ExerciseCompleted


class TrainingSessionCompletedAdmin(admin.ModelAdmin):
    list_display = ('get_session_title', 'get_date', 'date_completed')
    inlines = [ExerciseCompletedInLine]

    def get_session_title(self, obj):
        return obj.training_session.session_title

    def get_date(self, obj):
        return obj.training_session.date

    def training_session_link(self, obj):
        url = '/admin/muscu_site/trainingsession/' + obj.id + '/change/'
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.training_session.session_title))

    get_session_title.short_description = 'Titre de la séance'
    get_date.short_description = 'Date de création'
    training_session_link.short_description = "Lien de la séance d'origine"


admin.site.register(TrainingSession, TrainingSessionAdmin)
admin.site.register(TrainingSessionCompleted, TrainingSessionCompletedAdmin)
