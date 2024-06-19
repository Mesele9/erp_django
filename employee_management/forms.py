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
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile No'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Basic Salary'}),
            #'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Phone'}),
            'gender': forms.RadioSelect(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Employee Address', 'rows': 2}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file', 'description', 'employee']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        include_employee_field = kwargs.pop('include_employee_field', True)
        super().__init__(*args, **kwargs)

        if not include_employee_field:
            self.fields.pop('employee')  # Remove 'employee' field if not needed
        else:
            self.fields['employee'].queryset = Employee.objects.filter(is_active=True)


class EmployeeFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    search = forms.CharField(required=False)

