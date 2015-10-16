import json
import logging
from time import sleep

import redis
from django.conf import settings
from django.core.management import BaseCommand

from frigg.webhooks.events.github import GithubEvent

logger = logging.getLogger(__name__)

EVENT_SERVICES = {
    'github': GithubEvent
}


class Command(BaseCommand):
    help = 'Handle webhook events put on the queue.'

    def add_arguments(self, parser):
        parser.add_argument('--number', action='store', type=int, dest='number', default='-1')

    def handle(self, *args, **options):
        self.redis = redis.Redis(**settings.REDIS_SETTINGS)
        counter = 0

        while options['number'] == -1 or counter < options['number']:
            sleep(5)
            item = self.redis.rpop(settings.FRIGG_WEBHOOK_QUEUE)
            while item:
                sleep(0.5)
                self.handle_event(item)
                item = None

                if options['number'] != -1:
                    counter += 1

                if options['number'] == -1 or counter < options['number']:
                    item = self.redis.rpop(settings.FRIGG_WEBHOOK_QUEUE)

    def handle_event(self, item):
        try:
            parsed = json.loads(item.decode())
            event = EVENT_SERVICES[parsed['service']](parsed['type'], parsed['payload'])
            event.handle()
            self.stdout.write(event.response)
        except Exception as error:
            self.redis.lpush(settings.FRIGG_WEBHOOK_FAILED_QUEUE, item)
            raise error
