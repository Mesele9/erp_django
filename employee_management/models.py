from django.db import models
from .utils import document_upload_to
from ethiopian_date import EthiopianDateConverter

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    et_calendar = EthiopianDateConverter()

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    EDUCATION_LEVEL_CHOICES = (
        ('Master', 'Master\'s Degree'),
        ('Degree', 'Bachelor\'s Degree'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
        ('Grade', 'Grade'),
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pension_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    is_coc_certified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='employee_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name}"
    
    # Convert date of birth to gregorian date
    def gregorian_date_of_birth(self):
        if self.date_of_birth:
            ethiopian_date = self.date_of_birth
            converted_date = self.et_calendar.to_gregorian(ethiopian_date.year, ethiopian_date.month, ethiopian_date.day)
        else:
            None
        return converted_date
    
    # convert hire date to gregorian date
    def gregorian_hire_date(self):
        if self.hire_date:
            ethiopian_date = self.hire_date
            converted_date = self.et_calendar.to_gregorian(ethiopian_date.year, ethiopian_date.month, ethiopian_date.day)
        else:
            None
        return converted_date
    
    
class Document(models.Model):

    NAME_CHOICES = (
        ('educational_document', 'Educational Document'),
        ('kebele_id', 'Kebele ID'),
        ('employment', 'Employement Letter'),
        ('promotion', 'Promotions Letter'),
        ('demotion', 'Demotion Letter'),
        ('first_warning', 'First Warning'),
        ('second_warning', 'Second Warning'),
        ('third_warning', 'Third Warning'),
        ('final_warning', 'Final Warning'),
        ('termination', 'Termination Letter'),    
    )
    name = models.CharField(max_length=50, choices=NAME_CHOICES)
    file = models.FileField(upload_to=document_upload_to)
    description = models.TextField(blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

