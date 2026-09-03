from django.test import TestCase
from .services import REALTIME_EVENTS
class RealtimeTests(TestCase):
    def test_signal_event(self): self.assertIn('signal',REALTIME_EVENTS)
