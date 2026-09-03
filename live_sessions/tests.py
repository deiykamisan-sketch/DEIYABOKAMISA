from django.test import TestCase
from .models import AttendanceRecord
class AttendanceModelTests(TestCase):
    def test_model_name(self): self.assertEqual(AttendanceRecord._meta.model_name,'attendancerecord')
