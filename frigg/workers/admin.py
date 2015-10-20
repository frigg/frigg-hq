from django.contrib import admin

from .models import Dependency


class DependencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')


admin.site.register(Dependency, DependencyAdmin)
