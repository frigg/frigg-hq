from .base import Event


class GitlabEvent(Event):
    REPOSITORY_URL = '{event.repository_owner}/{event.repository_name}'
    ALLOWED_EVENT_TYPES = ['push', 'merge_request']

    @property
    def author(self):
        if self.event_type == 'push':
            return self.data['commits'][-1]['author']['name']
        if self.event_type == 'merge_request':
            return self.data['user']['username']

    @property
    def branch(self):
        if self.event_type == 'push':
            return self.data['ref'].replace('refs/heads/', '')
        if self.event_type == 'merge_request':
            return self.data['object_attributes']['source_branch']

    @property
    def _repository(self):
        if self.event_type == 'push':
            return self.data['repository']
        elif self.event_type == 'merge_request':
            return self.data['object_attributes']['target']

    @property
    def repository_owner(self):
        if self.event_type == 'push':
            return self._repository['git_http_url'].split('/')[-2]
        elif self.event_type == 'merge_request':
            return self._repository['http_url'].split('/')[-2]

    @property
    def repository_name(self):
        if self.event_type == 'push':
            return self._repository['git_http_url'].split('/')[-1].replace('.git', '')
        elif self.event_type == 'merge_request':
            return self._repository['http_url'].split('/')[-1].replace('.git', '')

    @property
    def repository_private(self):
        if self._repository:
            return self._repository['visibility_level'] == 20

    @property
    def hash(self):
        if self.event_type == 'push':
            return self.data['after']
        elif self.event_type == 'merge_request':
            return self.data['object_attributes']['last_commit']['id']

    @property
    def is_retest_comment_event(self):
        return False

    @property
    def pull_request_id(self):
        if self.event_type == 'merge_request':
            return self.data['object_attributes']['id']
        return 0

    @property
    def message(self):
        if self.event_type == 'push':
            return self.data['commits'][-1]['message']
        elif self.event_type == 'merge_request':
            return '{attributes[title]}\n{attributes[description]}'.format(
                attributes=self.data['object_attributes']
            )
