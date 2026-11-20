from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Department, Employee


class PanelTests(TestCase):
    def setUp(self):
        self.url = reverse('panel')
        self.admin = User.objects.create_superuser('boss', 'boss@example.com', 'pass12345')

    def login(self):
        self.client.force_login(self.admin)

    def test_anonymous_redirected_to_login(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse('admin:login'), r['Location'])

    def test_non_staff_redirected(self):
        user = User.objects.create_user('worker', password='pass12345')
        self.client.force_login(user)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_page_shows_seed_data(self):
        self.login()
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Backend-розробка')
        self.assertContains(r, 'Андрій Ткаченко')

    def test_department_crud(self):
        self.login()
        r = self.client.post(self.url, {'action': 'create_department', 'name': 'DevOps',
                                        'city': 'Лондон', 'founded_year': 2025, 'budget': '70000'},
                             follow=True)
        self.assertContains(r, 'додано')
        dep = Department.objects.get(name='DevOps')

        self.client.post(self.url, {'action': 'update_department', 'id': dep.id, 'name': 'DevOps & Cloud',
                                    'city': 'Париж', 'founded_year': 2025, 'budget': '90000'})
        dep.refresh_from_db()
        self.assertEqual((dep.name, dep.city, int(dep.budget)), ('DevOps & Cloud', 'Париж', 90000))

        self.client.post(self.url, {'action': 'delete_department', 'id': dep.id})
        self.assertFalse(Department.objects.filter(pk=dep.pk).exists())

    def test_employee_crud_and_cascade(self):
        self.login()
        dep = Department.objects.create(name='Тест', city='Одеса', founded_year=2026, budget=1000)
        self.client.post(self.url, {'action': 'create_employee', 'full_name': 'Іван Тестовий',
                                    'position': 'Стажер', 'department': dep.id, 'salary': '800',
                                    'hire_year': 2026, 'phone': '', 'is_remote': 'on'})
        emp = Employee.objects.get(full_name='Іван Тестовий')
        self.assertTrue(emp.is_remote)

        self.client.post(self.url, {'action': 'update_employee', 'id': emp.id, 'full_name': 'Іван Тестовий',
                                    'position': 'Junior', 'department': dep.id, 'salary': '1200',
                                    'hire_year': 2026, 'phone': '380000000000'})
        emp.refresh_from_db()
        self.assertEqual(emp.position, 'Junior')
        self.assertFalse(emp.is_remote)  # чекбокс не передано -> False

        self.client.post(self.url, {'action': 'delete_department', 'id': dep.id})
        self.assertFalse(Employee.objects.filter(pk=emp.pk).exists())  # CASCADE

    def test_invalid_input_shows_error_not_500(self):
        self.login()
        before = Department.objects.count()
        r = self.client.post(self.url, {'action': 'create_department', 'name': 'X', 'city': 'Одеса',
                                        'founded_year': 'abc', 'budget': '-5'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Помилка')
        self.assertEqual(Department.objects.count(), before)

    def test_unknown_action_and_missing_object(self):
        self.login()
        r = self.client.post(self.url, {'action': 'drop_tables'}, follow=True)
        self.assertContains(r, 'Невідома дія')
        r = self.client.post(self.url, {'action': 'delete_employee', 'id': 999999})
        self.assertEqual(r.status_code, 404)
