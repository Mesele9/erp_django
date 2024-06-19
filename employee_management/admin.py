from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from employee_management.models import Position, Department, Employee
from datetime import datetime

# Resource class for Employee import/export
class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'gender', 'department', 'position', 'date_of_birth', 'hire_date', 'salary')
        import_id_fields = ('id',)

    def before_import_row(self, row, **kwargs):
        # Convert department name to department ID (handle missing departments)
        department_name = row.get('department')
        if department_name:
            department = Department.objects.filter(name=department_name).first()
            if department:
                row['department'] = department.id
            else:
                # Handle missing department gracefully
                row['department'] = None  # or raise ValueError or handle differently

        # Convert position name to position ID (handle missing positions)
        position_name = row.get('position')
        if position_name:
            position = Position.objects.filter(name=position_name).first()
            if position:
                row['position'] = position.id
            else:
                # Handle missing position gracefully
                row['position'] = None  # or raise ValueError or handle differently

        # Validate date formats and convert datetime objects to strings
        date_of_birth_str = row.get('date_of_birth')
        if isinstance(date_of_birth_str, datetime):
            row['date_of_birth'] = date_of_birth_str.strftime('%Y-%m-%d')

        hire_date_str = row.get('hire_date')
        if isinstance(hire_date_str, datetime):
            row['hire_date'] = hire_date_str.strftime('%Y-%m-%d')

        return super().before_import_row(row, **kwargs)

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('first_name', 'middle_name', 'last_name', 'gender', 'department', 'position', 'date_of_birth', 'hire_date', 'salary', 'is_active')
    list_filter = ('department', 'position', 'gender', 'is_active')
    search_fields = ('first_name', 'last_name', 'department__name', 'position__name')
    ordering = ('first_name', 'last_name')


admin.site.register(Department)
admin.site.register(Position)
