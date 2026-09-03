from django.test import TestCase
from .models import UserPreference
class UsersModelTests(TestCase):
    def test_language_default(self): self.assertEqual(UserPreference._meta.get_field('language').default,'en')
