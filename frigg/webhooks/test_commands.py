import json
import os
from io import StringIO

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

    def test_command(self):
        r = redis.Redis(**settings.REDIS_SETTINGS)
        r.lpush(settings.FRIGG_WEBHOOK_QUEUE, json.dumps({
            'service': 'github',
            'type': 'ping',
            'payload': self.load_fixture('ping.json')
        }))
        out = StringIO()
        call_command('fetch_webhook_payload', number=1, stdout=out)
        self.assertIn('Handled "ping"', out.getvalue())
