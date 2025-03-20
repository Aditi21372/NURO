from django.test import TestCase
from .models import Task
from django.urls import reverse
from django.core.exceptions import ValidationError

class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            priority=3,
            deadline='2023-12-31 12:00:00'
        )


    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.priority, 3)
        self.assertFalse(self.task.completed)


    def test_priority_validation(self):
        with self.assertRaises(ValidationError):
            task = Task(title='Invalid Task', priority=6)
            task.clean()  # This should raise a ValidationError


class ManageTaskViewTest(TestCase):
    def test_manage_task_view(self):
        response = self.client.post(reverse('manage_task'), {'task_name': 'New Task'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task created successfully!')

    def test_manage_task_view_no_task_name(self):
        response = self.client.post(reverse('manage_task'), {'task_name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task name cannot be empty.')


    def test_manage_task_view_no_task_name(self):
        response = self.client.post(reverse('manage_task'), {'task_name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task name cannot be empty.')
