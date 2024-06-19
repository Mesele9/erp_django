
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import Item, Category, Subcategory, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ('id', 'description', 'category', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock')

@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource
    list_display = ('description', 'category', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock')
    search_fields = ('description', 'category')


class PurchaseRecordItemInline(admin.TabularInline):
    model = PurchaseRecordItem
    extra = 1

class PurchaseRecordAdmin(admin.ModelAdmin):
    inlines = [PurchaseRecordItemInline]


admin.site.register(PurchaseRecord, PurchaseRecordAdmin)
admin.site.register(IssueRecord)


admin.site.register(Category)
admin.site.register(Subcategory)

