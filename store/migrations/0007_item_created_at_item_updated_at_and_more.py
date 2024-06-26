# Generated by Django 4.2.11 on 2024-06-29 03:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0016_alter_document_name'),
        ('store', '0006_alter_subcategory_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='issuerecord',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.department'),
        ),
        migrations.AlterField(
            model_name='item',
            name='current_unit_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='minimum_stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='stock_balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='unit_of_measurement',
            field=models.CharField(choices=[('pcs', 'Piece'), ('kg', 'Kilogram'), ('gm', 'Gram'), ('lt', 'Liter'), ('bot', 'Bottle'), ('carton', 'Carton'), ('crate', 'Crate'), ('pac', 'Pack'), ('box', 'Box'), ('keg', 'Keg'), ('dz', 'Dozen'), ('m', 'Meter')], max_length=50),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='tin_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
