from django.test import TestCase
from .services import valid_canvas_image
class WhiteboardTests(TestCase):
    def test_rejects_non_image(self): self.assertFalse(valid_canvas_image('bad'))
