# -*- coding: utf8 -*-
from django.contrib import admin
from django.template.defaultfilters import pluralize

from .models import Build, BuildResult, Project


class BuildResultInline(admin.StackedInline):
    model = BuildResult
    readonly_fields = ('result_log', 'succeeded')
    extra = 0
    max_num = 0


class BuildInline(admin.TabularInline):
    model = Build
    readonly_fields = ('build_number', 'branch', 'color', 'pull_request_id', 'sha')
    extra = 0
    max_num = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'git_repository', 'average_time', 'last_build_number')
    inlines = [BuildInline]
    list_filter = ['owner']


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('build_number', 'project', 'branch', 'pull_request_id', 'sha', 'color')
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
class BuildResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'succeeded', 'coverage')
