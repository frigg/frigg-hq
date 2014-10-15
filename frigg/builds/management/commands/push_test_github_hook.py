# -*- coding: utf8 -*-
import json
import requests
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        fixtures_path = os.path.join(settings.BASE_DIR, 'helpers/fixtures/github')
        data = json.load(open(os.path.join(fixtures_path, 'push_master.json')))

        r = requests.post("http://localhost:8000/webhooks/github/",
                          data=json.dumps(data),
                          headers={'X-GitHub-Event': "push"})
        print r.text
