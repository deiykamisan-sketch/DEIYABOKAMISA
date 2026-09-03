from importlib import import_module
from django.test import SimpleTestCase


class ProjectStructureTests(SimpleTestCase):
    def test_all_architecture_modules_are_importable(self):
        modules = [
            'accounts', 'users', 'lectures', 'live_sessions', 'whiteboard',
            'camera', 'pen_tracking', 'recording', 'speech', 'ai',
            'questions', 'realtime', 'chat', 'notifications', 'sharing',
        ]
        for module in modules:
            with self.subTest(module=module):
                self.assertIsNotNone(import_module(module))
