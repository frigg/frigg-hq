from django.contrib import admin
from django.template.defaultfilters import pluralize

from .forms import EnvironmentVariableForm
from .models import EnvironmentVariable, Project


class EnvironmentVariableMixin:
    form = EnvironmentVariableForm

    @staticmethod
    def get_readonly_fields(request, obj=None):
        if obj:
            return 'key', 'value', 'is_secret'
        return tuple()


class EnvironmentVariableInline(EnvironmentVariableMixin, admin.TabularInline):
    model = EnvironmentVariable
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'queue_name', 'approved', 'number_of_members', 'average_time',
                    'last_build_number', 'can_deploy')
    list_filter = ['owner', 'queue_name', 'approved', 'can_deploy']
    actions = ['sync_members']
    inlines = [EnvironmentVariableInline]

    def sync_members(self, request, queryset):
        for project in queryset:
            project.update_members()

        self.message_user(
            request,
            '{} project{} was synced'.format(len(queryset), pluralize(len(queryset)))
        )

    sync_members.short_description = 'Sync members of selected projects'


@admin.register(EnvironmentVariable)
class EnvironmentVariableAdmin(EnvironmentVariableMixin, admin.ModelAdmin):
    list_display = (
        '__str__',
        'is_secret',
    )
