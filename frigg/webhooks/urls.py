from django.conf.urls import url

from .views import GithubWebhookView

urlpatterns = [
    url(r'^github/$', GithubWebhookView.as_view(), name='github'),
]
