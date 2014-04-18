from django.contrib import admin
from frigg.builds.models import Build, BuildResult

admin.site.register(Build)
admin.site.register(BuildResult)