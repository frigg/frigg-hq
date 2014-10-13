# -*- coding: utf8 -*-
from django.contrib import admin

from frigg.builds.models import Build, BuildResult, Project

admin.site.register(Project)
admin.site.register(Build)
admin.site.register(BuildResult)
