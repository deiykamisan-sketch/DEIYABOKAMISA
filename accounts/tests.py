from django.test import TestCase
from .models import UserRole
class AccountsModelTests(TestCase):
    def test_role_default(self): self.assertEqual(UserRole._meta.get_field('role').default,'student')
