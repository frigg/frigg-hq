from django.contrib import admin

from .models import Worker


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')


admin.site.register(Worker, WorkerAdmin)
