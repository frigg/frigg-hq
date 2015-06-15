from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from frigg.utils.tests import ViewTestCase


class ReactViewTest(ViewTestCase):

    def test_view_should_return_200(self):
        self.assertStatusCode(self.client.get(reverse('react_view')))

    @override_settings(JS_SENTRY_DSN='DSN')
    def test_view_should_contain_sentry_dsn(self):
        self.assertContains(self.client.get(reverse('react_view')), 'DSN')

    def test_view_should_contain_user_data(self):
        self.assertContains(self.client.get(reverse('react_view')), 'window.user')

    def test_cache_manifest(self):
        self.assertStatusCode(self.client.get(reverse('manifest')))
