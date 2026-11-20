from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

CITY_CHOICES = [
    ('Одеса', 'Одеса'),
    ('Лондон', 'Лондон'),
    ('Париж', 'Париж'),
    ('Відень', 'Відень'),
]


class Department(models.Model):
    """Відділ компанії (аналог Author з прикладу)."""
    name = models.CharField('Назва', max_length=100, unique=True)
    city = models.CharField('Місто', max_length=30, choices=CITY_CHOICES, default='Одеса')
    founded_year = models.PositiveIntegerField(
        'Рік створення', validators=[MinValueValidator(2008), MaxValueValidator(2100)])
    budget = models.DecimalField(
        'Бюджет, $', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Відділ'
        verbose_name_plural = 'Відділи'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} ({self.city})'


class Employee(models.Model):
    """Працівник відділу (аналог Book з прикладу)."""
    full_name = models.CharField("Ім'я та прізвище", max_length=120)
    position = models.CharField('Посада', max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='employees', verbose_name='Відділ')
    salary = models.DecimalField(
        'Зарплата, $', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hire_year = models.PositiveIntegerField(
        'Рік прийому', validators=[MinValueValidator(2008), MaxValueValidator(2100)])
    phone = models.CharField('Телефон', max_length=20, blank=True)
    is_remote = models.BooleanField('Віддалено', default=False)

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['-id']

    def __str__(self):
        return self.full_name
