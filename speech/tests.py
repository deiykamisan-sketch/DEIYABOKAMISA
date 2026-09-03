from django.test import TestCase
from .models import TranscriptSegment
class SpeechTests(TestCase):
    def test_ordering(self): self.assertEqual(TranscriptSegment._meta.ordering,['start_ms'])
