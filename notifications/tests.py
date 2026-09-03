from django.test import TestCase
from .services import NOTIFICATION_TYPES
class NotificationTests(TestCase):
    def test_question_notification(self): self.assertIn('question',NOTIFICATION_TYPES)
