# -*- coding: utf8 -*-
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from frigg.webhooks.events.github import GithubEvent
from frigg.webhooks.events.gitlab import GitlabEvent


class WebhookView(View):
    """
    A generic webhook view. It should be extended and ``get_event_type`` and ``get_event_object``
    should be overridden.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebhookView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        event_type = self.get_event_type(request)
        if not event_type:
            return HttpResponse('Missing HTTP_X_GITHUB_EVENT')

        event = self.get_event_object(request, event_type)
        event.handle()
        return HttpResponse(event.response)

    def get_event_type(self, request):
        raise NotImplementedError

    def get_event_object(self, request, event_type):
        raise NotImplementedError


class GithubWebhookView(WebhookView):

    def get_event_type(self, request):
        try:
            return request.META['HTTP_X_GITHUB_EVENT']
        except KeyError:
            return None

    def get_event_object(self, request, event_type):
        data = json.loads(str(request.body, encoding='utf-8'))
        return GithubEvent(event_type, data)


class GitlabWebhookView(WebhookView):

    def get_event_type(self, request):
        data = json.loads(str(request.body, encoding='utf-8'))
        return data['object_kind']

    def get_event_object(self, request, event_type):
        data = json.loads(str(request.body, encoding='utf-8'))
        return GitlabEvent(event_type, data)
