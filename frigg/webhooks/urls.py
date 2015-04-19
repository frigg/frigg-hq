from django.conf.urls import url

from .views import GithubWebhookView, GitlabWebhookView

urlpatterns = [
    url(r'^github/$', GithubWebhookView.as_view(), name='github'),
    url(r'^gitlab/$', GitlabWebhookView.as_view(), name='gitlab'),
]
