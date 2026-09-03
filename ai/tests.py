from django.test import TestCase
from .services import AI_FEATURES
class AITests(TestCase):
    def test_summary_feature(self): self.assertIn('summary',AI_FEATURES)
