from django.test import TestCase
from .services import QUESTION_STATES
class QuestionTests(TestCase):
    def test_answered_state(self): self.assertIn('answered',QUESTION_STATES)
