from frigg.helpers.common import is_retest_comment

from .base import Event


class GithubEvent(Event):
    REPOSITORY_URL = 'git@github.com:{event.repository_owner}/{event.repository_name}.git'
    ALLOWED_EVENT_TYPES = ['ping', 'push', 'pull_request', 'issue_comment']
    ALLOWED_PULL_REQUEST_ACTIONS = ['open', 'synchronize']
    ALLOWED_COMMENT_EVENTS = ['issue_comment']

    @property
    def repository_owner(self):
        try:
            if 'name' in self.data['repository']['owner']:
                return self.data['repository']['owner']['name']
            return self.data['repository']['owner']['login']
        except KeyError:
            return None

    @property
    def repository_name(self):
        try:
            return self.data['repository']['name']
        except KeyError:
            return None

    @property
    def repository_private(self):
        try:
            return self.data['repository']['private']
        except KeyError:
            return None

    @property
    def branch(self):
        if self.event_type == 'push':
            if self.data['ref'].startswith('refs/tags/'):
                return 'tag/{0}'.format(self.data['ref'].replace('refs/tags/', ''))
            return self.data['ref'][11:]
        elif self.event_type == 'pull_request':
            return self.data['pull_request']['head']['ref']

    @property
    def hash(self):
        if self.event_type == 'push':
            return self.data['after']
        elif self.event_type == 'pull_request':
            return self.data['pull_request']['head']['sha']

    @property
    def pull_request_id(self):
        if self.event_type == 'pull_request':
            return self.data['number']
        elif self.event_type == 'issue_comment':
            return int(self.data['issue']['pull_request']['url'].split("/")[-1])
        return 0

    @property
    def commit(self):
        if len(self.data['commits']):
            return self.data['commits'][-1]
        elif 'head_commit' in self.data:
            return self.data['head_commit']

    @property
    def author(self):
        if self.event_type == 'push':
            return self.commit['author']['username']
        elif self.event_type == 'pull_request':
            return self.data['pull_request']['user']['login']

    @property
    def message(self):
        if self.event_type == 'push':
            return self.commit['message']
        elif self.event_type == 'pull_request':
            return '{}\n{}'.format(
                self.data['pull_request']['title'] or '',
                self.data['pull_request']['body'] or ''
            )

    @property
    def is_unknown_event_type(self):
        if self.event_type == 'pull_request':
            return self.data['action'] not in self.ALLOWED_PULL_REQUEST_ACTIONS
        else:
            return super().is_unknown_event_type

    @property
    def is_retest_comment_event(self):
        if self.event_type in self.ALLOWED_COMMENT_EVENTS:
            return is_retest_comment(self.data['comment']['body'])
        return False
