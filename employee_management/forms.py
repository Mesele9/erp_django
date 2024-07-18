from django import forms
from django.forms import inlineformset_factory
from .models import Employee, Department, Position, Document


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'mobile',
                  'email', 'department', 'position', 'date_of_birth', 'hire_date',
                  'salary', 'education_level', 'address', 'pension_number',
                  'emergency_contact_name', 'emergency_contact_phone',
                  'is_coc_certified', 'is_active', 'picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'gender': forms.RadioSelect(),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile No'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Basic Salary'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Address', 'rows':2}),
            'pension_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pension Number'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Phone'}),
            'is_coc_certified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EmployeeFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    search = forms.CharField(required=False)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file', 'description', 'employee']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        include_employee_field = kwargs.pop('include_employee_field', True)
        super().__init__(*args, **kwargs)

        if not include_employee_field:
            self.fields.pop('employee')  # Remove 'employee' field if not needed
        else:
            self.fields['employee'].queryset = Employee.objects.filter(is_active=True)



