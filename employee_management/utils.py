import os
from django.utils.text import slugify
from ethiopian_date import EthiopianDateConverter
from datetime import timedelta, datetime, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def document_upload_to(instance, file_name):
  """
  Generates a unique upload path for documents based on employee ID and file name.

  Args:
      instance (Document): The Document object being saved.

  Returns:
      str: The upload path for the file.
  """
  # Ensure employee object is available
  if not instance.employee:
    raise ValueError("Employee object is not set for the Document instance.")

  # Create a slugified version of the file name (optional for better URL compatibility)
  #file_name = slugify(instance.file.name)
  file_base_name = os.path.basename(file_name)


  # Construct the upload path using employee ID and slugified file name
  return f'documents/{instance.employee.id}/{file_base_name}'


# Convert date of  birth and calculate employees whose birthdays is comming in a week time
def is_upcoming_birthday(employee):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    et_calendar = EthiopianDateConverter()
    gregorian_dob = et_calendar.to_gregorian(employee.date_of_birth.year, employee.date_of_birth.month, employee.date_of_birth.day)
  
    return gregorian_dob.month == today.month and gregorian_dob.day in range(today.day, next_week.day)


# Convert hire date and calculate service durations of employees
def calculate_service_duration(ethiopian_hire_date):
    converter = EthiopianDateConverter()
    today = timezone.now().date()

    gregorian_hire_date = converter.to_gregorian(
        ethiopian_hire_date.year, ethiopian_hire_date.month, ethiopian_hire_date.day
    )
    service_duration = relativedelta(today, gregorian_hire_date)

    if service_duration.years > 0:
        return f"{service_duration.years} year, {service_duration.months} month and {service_duration.days} day"
    elif service_duration.months > 0:
        return f"{service_duration.months} month and {service_duration.days} day"
    else:
        return f"{service_duration.days} days"
  