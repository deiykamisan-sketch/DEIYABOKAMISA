from django.test import TestCase
from .services import MAX_MESSAGE_LENGTH
class ChatTests(TestCase):
    def test_message_limit(self): self.assertEqual(MAX_MESSAGE_LENGTH,500)
