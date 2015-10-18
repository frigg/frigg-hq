import json
import os
from io import StringIO
from unittest import mock

import redis
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase


class FetchWebhookPayloadCommandTests(TestCase):
    fixtures = ['frigg/builds/fixtures/users.json']
    FIXTURE_PATH = 'webhooks/fixtures/github'

    def load_fixture(self, fixture):
        fixtures_path = os.path.join(settings.BASE_DIR, self.FIXTURE_PATH, fixture)
        return json.load(open(fixtures_path, encoding='utf-8'))

    def setUp(self):
        self.maxDiff = None
        self.redis = redis.Redis(**settings.REDIS_SETTINGS)
        self.item = {
            'service': 'github',
            'type': 'ping',
            'payload': self.load_fixture('ping.json'),
        }
        self.redis.lpush(settings.FRIGG_WEBHOOK_QUEUE, json.dumps(self.item))

    def test_command(self):
        out = StringIO()
        call_command('fetch_webhook_payload', number=1, stdout=out)
        self.assertIn('Handled "ping"', out.getvalue())

    @mock.patch('frigg.webhooks.events.github.GithubEvent.handle', side_effect=RuntimeError("fail"))
    def test_command_handle_event_failure(self, mock_handle):
        out = StringIO()
        with self.assertRaises(RuntimeError):
            call_command('fetch_webhook_payload', number=1, stdout=out)
        item = self.redis.rpop(settings.FRIGG_WEBHOOK_FAILED_QUEUE).decode()
        self.assertEqual(json.loads(item), self.item)
