from django.test import TestCase
from .services import VISIBILITY_LEVELS
class SharingTests(TestCase):
    def test_private_visibility(self): self.assertIn('private',VISIBILITY_LEVELS)
