from decimal import Decimal

from django.db import migrations

DEPARTMENTS = [
    ('Керівництво', 'Одеса', 2008, '250000'),
    ('Backend-розробка', 'Одеса', 2009, '420000'),
    ('Frontend-розробка', 'Лондон', 2014, '310000'),
    ('Тестування (QA)', 'Париж', 2017, '180000'),
    ('HR та навчання', 'Відень', 2020, '95000'),
]

EMPLOYEES = [
    ('Олександр Коваленко', 'Генеральний директор', 'Керівництво', '9500', 2008, '380671112233', False),
    ('Марина Шевченко', 'Технічний директор', 'Керівництво', '9000', 2009, '380502223344', False),
    ('Дмитро Бондар', 'Операційний директор', 'Керівництво', '8200', 2008, '380933334455', False),
    ('Ірина Мельник', 'Директор з персоналу', 'HR та навчання', '6500', 2012, '380674445566', False),
    ('Андрій Ткаченко', 'Senior Python-розробник', 'Backend-розробка', '5200', 2015, '380631234567', True),
    ('Оксана Литвин', 'Django-розробник', 'Backend-розробка', '3800', 2021, '380975556677', False),
    ('James Carter', 'React-розробник', 'Frontend-розробка', '4600', 2016, '447700900123', False),
    ('Софія Романенко', 'UI/UX-дизайнер', 'Frontend-розробка', '3500', 2022, '380661112200', True),
    ('Claire Dubois', 'QA Lead', 'Тестування (QA)', '4100', 2017, '33612345678', False),
    ('Тарас Гнатюк', 'QA-інженер', 'Тестування (QA)', '2600', 2024, '380687778899', True),
]


def seed(apps, schema_editor):
    Department = apps.get_model('panel', 'Department')
    Employee = apps.get_model('panel', 'Employee')
    deps = {}
    for name, city, year, budget in DEPARTMENTS:
        deps[name] = Department.objects.create(
            name=name, city=city, founded_year=year, budget=Decimal(budget))
    for full_name, position, dep, salary, year, phone, remote in EMPLOYEES:
        Employee.objects.create(
            full_name=full_name, position=position, department=deps[dep],
            salary=Decimal(salary), hire_year=year, phone=phone, is_remote=remote)


def unseed(apps, schema_editor):
    apps.get_model('panel', 'Department').objects.filter(
        name__in=[d[0] for d in DEPARTMENTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
