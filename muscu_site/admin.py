from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import TrainingSession, Exercise, TrainingSessionCompleted, ExerciseCompleted


class ExerciseInLine(admin.TabularInline):
    model = Exercise


class TrainingSessionAdmin(admin.ModelAdmin):
    inlines = [ExerciseInLine]


class ExerciseCompletedInLine(admin.TabularInline):
    model = ExerciseCompleted


class TrainingSessionCompletedAdmin(admin.ModelAdmin):
    list_display = ('get_session_title', 'get_date', 'date_completed', 'training_session_link')
    inlines = [ExerciseCompletedInLine]

    def get_session_title(self, obj):
        return obj.training_session.session_title

    get_session_title.admin_order_field = 'training_session__session_title'

    def get_date(self, obj):
        return obj.training_session.date

    get_date.admin_order_field = 'training_session__date'

    def training_session_link(self, obj):
        url = reverse('admin:muscu_site_trainingsessioncompleted_change', kwargs={'object_id': obj.id})
        return format_html("<a href='{}'>{}</a>", url, obj.training_session.session_title)

    get_session_title.short_description = 'Titre de la séance'
    get_date.short_description = 'Date de création'
    training_session_link.short_description = "Lien de la séance d'origine"


admin.site.register(TrainingSession, TrainingSessionAdmin)
admin.site.register(TrainingSessionCompleted, TrainingSessionCompletedAdmin)
