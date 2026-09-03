from django.test import TestCase
from .services import RECORDING_STATES
class RecordingTests(TestCase):
    def test_ready_state(self): self.assertIn('ready',RECORDING_STATES)
