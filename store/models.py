from django.db import models
from employee_management.models import Department
from django.utils import timezone


class Supplier(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    tin_number = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):

    UNIT_OF_MEASUREMENT_CHOICES = [
        ('pcs', 'Piece'),
        ('kg', 'Kilogram'),
        ('gm', 'Gram'),
        ('lt', 'Liter'),
        ('bot', 'Bottle'),
        ('carton', 'Carton'),
        ('crate', 'Crate'),
        ('pac', 'Pack'),
        ('box', 'Box'),
        ('keg', 'Keg'),
        ('dz', 'Dozen'),
        ('m', 'Meter'),
    ]
    
    description = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE, db_index=True)
    subcategory = models.ForeignKey(Subcategory, related_name='items', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    unit_of_measurement = models.CharField(max_length=50, choices=UNIT_OF_MEASUREMENT_CHOICES)
    current_unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_balance = models.PositiveIntegerField()
    minimum_stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.description

class PurchaseRecord(models.Model):
    date = models.DateField(default=timezone.now)
    supplier = models.ForeignKey(Supplier, related_name='supplier', on_delete=models.CASCADE, null=True)
    purchaser = models.CharField(max_length=100)
    voucher_number = models.CharField(max_length=50, unique=True, null=True, db_index=True)
    upload_receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    
    def __str__(self):
        return f'Purchase Record {self.voucher_number} - {self.date} {self.total_value}'

    @property
    def total_value(self):
        return sum(item.total_price for item in self.items.all())

    def delete(self, using=None, keep_parents=False):
        for item in self.items.all():
            item.item.stock_balance -= item.quantity
            item.item.save()
        super().delete(using=using, keep_parents=keep_parents)
    
    
class PurchaseRecordItem(models.Model):
    purchase_record = models.ForeignKey(PurchaseRecord, related_name='items', on_delete=models.CASCADE, db_index=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old = PurchaseRecordItem.objects.get(pk=self.pk)
            quantity_diff = self.quantity - old.quantity
            self.item.stock_balance += quantity_diff
        else:
            self.item.stock_balance += self.quantity
        
        self.total_price = self.quantity * self.unit_price
        self.item.current_unit_price = self.unit_price
        self.item.save()
        super().save(*args, **kwargs)
        self.purchase_record.total_value()
    
    def delete(self, *args, **kwargs):
        self.item.stock_balance -= self.quantity
        self.item.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f'{self.quantity} x {self.item.description}'

class IssueRecord(models.Model):
    date = models.DateField(default=timezone.now)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_index=True)
    issued_by = models.CharField(max_length=100)
    received_by = models.CharField(max_length=100)
    voucher_number = models.CharField(max_length=50, unique=True, null=True, db_index=True)

    def total_value(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f'Issue Record {self.voucher_number} - {self.date} {self.total_value}'
    
    def delete(self, using=None, keep_parents=False):
            for item in self.items.all():
                item.item.stock_balance += item.quantity
                item.item.save()
            super().delete(using=using, keep_parents=keep_parents)

class IssueRecordItem(models.Model):
    issue_record = models.ForeignKey(IssueRecord, related_name='items', on_delete=models.CASCADE, db_index=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old = IssueRecordItem.objects.get(pk=self.pk)
            quantity_diff = self.quantity - old.quantity
            self.item.stock_balance -= quantity_diff
        else:
            self.item.stock_balance -= self.quantity
        
        self.unit_price = self.item.current_unit_price
        self.total_price = self.quantity * self.unit_price
        self.item.save()
        super().save(*args, **kwargs)
        self.issue_record.total_value()
    
    def delete(self, *args, **kwargs):
        self.item.stock_balance += self.quantity
        self.item.save()
        super().delete(*args, **kwargs)    
    
    def __str__(self):
        return f'{self.quantity} x {self.item.description}'
    
