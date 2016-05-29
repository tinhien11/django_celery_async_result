from django.test import TestCase
from django.test.utils import override_settings
from app.tasks import add


class AddTestCase(TestCase):
    @override_settings(
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_ALWAYS_EAGER=True,
        BROKER_BACKEND='memory')
    def test_add_task(self):
        result = add.delay('1', '2')
        self.assertTrue(result.successful())
        self.assertEqual(result.result, '12', "Should return 12 on add string 1 and 2")
