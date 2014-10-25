# -*- coding: utf8 -*-
from django.contrib import admin

from .models import Build, BuildResult, Project


class BuildResultInline(admin.StackedInline):
    model = BuildResult
    readonly_fields = ('result_log', 'succeeded', 'return_code')
    extra = 0
    max_num = 0


class BuildInline(admin.TabularInline):
    model = Build
    readonly_fields = ('build_number', 'branch', 'color', 'pull_request_id', 'sha')
    extra = 0
    max_num = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'git_repository', 'average_time', 'user', 'last_build_number')
    inlines = [BuildInline]


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('build_number', 'project', 'branch', 'pull_request_id', 'sha', 'color')
    inlines = [BuildResultInline]


@admin.register(BuildResult)
class BuildResultAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'succeeded', 'return_code')
