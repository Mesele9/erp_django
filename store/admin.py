
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import Item, Category, Subcategory, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ('id', 'description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock')

    def before_import_row(self, row, **kwargs):
        # Convert department name to department ID (handle missing departments)
        category_name = row.get('category')
        if category_name:
            category = Category.objects.filter(name=category_name).first()
            if category:
                row['category'] = category.id
            else:
                # Handle missing department gracefully
                row['category'] = None  # or raise ValueError or handle differently

        # Convert position name to position ID (handle missing positions)
        subcategory_name = row.get('subcategory')
        if subcategory_name:
            subcategory = Subcategory.objects.filter(name=subcategory_name).first()
            if subcategory:
                row['subcategory'] = subcategory.id
            else:
                # Handle missing position gracefully
                row['subcategory'] = None  # or raise ValueError or handle differently

@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource
    list_display = ('description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock')
    search_fields = ('description', 'category', 'subcategory')


class PurchaseRecordItemInline(admin.TabularInline):
    model = PurchaseRecordItem
    extra = 1

class PurchaseRecordAdmin(admin.ModelAdmin):
    inlines = [PurchaseRecordItemInline]


admin.site.register(PurchaseRecord, PurchaseRecordAdmin)
admin.site.register(IssueRecord)


admin.site.register(Category)
admin.site.register(Subcategory)

