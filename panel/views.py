from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm, EmployeeForm
from .models import Department, Employee

# action -> (модель, форма, назва для повідомлень)
ENTITIES = {
    'department': (Department, DepartmentForm, 'Відділ'),
    'employee': (Employee, EmployeeForm, 'Працівника'),
}


def _form_errors(form):
    return '; '.join(f'{form.fields[f].label if f in form.fields else f}: {" ".join(e)}'
                     for f, e in form.errors.items())


@staff_member_required(login_url='admin:login')
def index(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        verb, _, entity = action.partition('_')  # create_department -> create, department
        if entity not in ENTITIES or verb not in ('create', 'update', 'delete'):
            messages.error(request, 'Невідома дія.')
            return redirect('panel')

        model, form_class, label = ENTITIES[entity]

        if verb == 'delete':
            obj = get_object_or_404(model, pk=request.POST.get('id'))
            obj.delete()
            messages.success(request, f'{label} «{obj}» видалено.')
            return redirect('panel')

        instance = get_object_or_404(model, pk=request.POST.get('id')) if verb == 'update' else None
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            done = 'додано' if verb == 'create' else 'оновлено'
            messages.success(request, f'{label} «{obj}» {done}.')
        else:
            messages.error(request, f'Помилка: {_form_errors(form)}')
        return redirect('panel')

    departments = Department.objects.annotate(emp_count=Count('employees'))
    employees = Employee.objects.select_related('department')
    context = {
        'title': 'Адмінка',
        'departments': departments,
        'employees': employees,
        'city_choices': Department._meta.get_field('city').choices,
        'total_salary': employees.aggregate(s=Sum('salary'))['s'] or 0,
    }
    return render(request, 'panel/admin.html', context)
