from django.contrib import admin
from .models import Department, Employee


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'founded_year', 'budget')
    list_filter = ('city',)
    search_fields = ('name',)
    inlines = [EmployeeInline]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'position', 'department', 'salary', 'hire_year', 'is_remote')
    list_filter = ('department', 'is_remote')
    search_fields = ('full_name', 'position')
