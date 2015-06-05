from django.contrib import admin
from django.template.defaultfilters import pluralize

from frigg.deployments.models import PRDeployment


@admin.register(PRDeployment)
class PRDeploymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'succeeded', 'port', 'ttl', 'image')
    list_filter = ['build__project']
    actions = ['redeploy']

    def redeploy(self, request, queryset):
        for deployment in queryset:
            deployment.start()

        self.message_user(
            request,
            '{} deployment{} was redeployed'.format(len(queryset), pluralize(len(queryset)))
        )

    redeploy.short_description = 'Redeploy selected deployments'
