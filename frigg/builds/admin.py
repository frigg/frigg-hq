# -*- coding: utf8 -*-
from django.contrib import admin
from django.template.defaultfilters import pluralize

from .models import Build, BuildResult


class BuildResultMixin(object):
    readonly_fields = (
        'worker_host',
        'build',
        'service_log',
        'setup_log',
        'result_log',
        'after_log',
        'succeeded',
        'still_running'
    )


class BuildResultInline(BuildResultMixin, admin.StackedInline):
    model = BuildResult
    extra = 0
    max_num = 0


class BuildInline(admin.TabularInline):
    model = Build
    readonly_fields = ('build_number', 'branch', 'color', 'pull_request_id', 'sha')
    extra = 0
    max_num = 0


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('build_number', 'project', 'branch', 'pull_request_id', 'sha', 'color')
    readonly_fields = ('build_number', 'project', 'branch', 'pull_request_id', 'sha', 'color',
                       'message', 'start_time', 'end_time', 'author')
    inlines = [BuildResultInline]
    list_filter = ['project']
    actions = ['restart_build']

    def restart_build(self, request, queryset):
        for build in queryset:
            build.start()

        self.message_user(
            request,
            '{} build{} was restarted'.format(len(queryset), pluralize(len(queryset)))
        )

    restart_build.short_description = 'Restart selected builds'


@admin.register(BuildResult)
class BuildResultAdmin(BuildResultMixin, admin.ModelAdmin):
    list_display = ('__str__', 'worker_host', 'succeeded', 'still_running', 'coverage')
