from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from employee_management.models import Position, Department, Employee
from datetime import datetime

# Resource class for Employee import/export
class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'gender', 'department', 'position', 'date_of_birth', 'hire_date', 'salary', 'education_level', 'address', 'pension_number', 'emergency_contact_name','emergency_contact_phone', 'is_coc_certified', 'is_active', 'picture')
        import_id_fields = ('id',)

    def before_import_row(self, row, **kwargs):
        # Convert department name to department ID (handle missing departments)
        if 'department_name' in row:
            department_name = row['department_name']
            try:
                department = Department.objects.get(name=department_name)
                row['department_id'] = department.id
            except Department.DoesNotExist:
                # Handle the case where department is not found
                pass

        # Map position_name to position_id if position_id is expected
        if 'position_name' in row:
            position_name = row['position_name']
            try:
                position = Position.objects.get(name=position_name)
                row['position_id'] = position.id
            except Position.DoesNotExist:
                # Handle the case where position is not found
                pass

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



# Resource class for Department import/export
class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = ('id', 'name')
        import_id_fields = ('id',)

# Resource class for Position import/export
class PositionResource(resources.ModelResource):
    class Meta:
        model = Position
        fields = ('id', 'name')
        import_id_fields = ('id',)


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    resource_class = PositionResource
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

#admin.site.register(Department)
#admin.site.register(Position)
