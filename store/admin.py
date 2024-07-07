
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import Item, Category, Subcategory, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem

class ItemResource(resources.ModelResource):
    category = fields.Field(column_name='category')
    subcategory = fields.Field(column_name='subcategory')

    class Meta:
        model = Item
        fields = ('id', 'description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock')
        export_order = ('id', 'description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock')

    def dehydrate_category(self, item):
        return item.category.name if item.category else ''

    def dehydrate_subcategory(self, item):
        return item.subcategory.name if item.subcategory else ''

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

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name')
        export_order = ('id', 'name')

class SubcategoryResource(resources.ModelResource):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category')
        export_order = ('id', 'name', 'category')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(ImportExportModelAdmin):
    resource_class = SubcategoryResource
    list_display = ('id', 'name', 'category')
    search_fields = ('name', 'category__name')


class PurchaseRecordItemInline(admin.TabularInline):
    model = PurchaseRecordItem
    extra = 1

class PurchaseRecordAdmin(admin.ModelAdmin):
    inlines = [PurchaseRecordItemInline]


admin.site.register(PurchaseRecord, PurchaseRecordAdmin)
admin.site.register(IssueRecord)