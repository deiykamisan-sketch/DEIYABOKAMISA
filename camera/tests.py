from django.test import TestCase
from .services import SUPPORTED_VIDEO_MIME_TYPES
class CameraTests(TestCase):
    def test_webm_supported(self): self.assertIn('video/webm',SUPPORTED_VIDEO_MIME_TYPES)
