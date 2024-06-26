# Generated by Django 4.2.11 on 2024-06-29 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0015_remove_leaverequest_employee_delete_attendance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(choices=[('educational_document', 'Educational Document'), ('kebele_id', 'Kebele ID'), ('employment', 'Employement Letter'), ('promotion', 'Promotions Letter'), ('demotion', 'Demotion Letter'), ('first_warning', 'First Warning'), ('second_warning', 'Second Warning'), ('third_warning', 'Third Warning'), ('final_warning', 'Final Warning'), ('termination', 'Termination Letter')], max_length=50),
        ),
    ]
