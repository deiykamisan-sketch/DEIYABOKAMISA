from django.test import TestCase
from .services import PenPoint
class PenTrackingTests(TestCase):
    def test_point(self): self.assertTrue(PenPoint(1,2).detected)
