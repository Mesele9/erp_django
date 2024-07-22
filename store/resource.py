from import_export import resources, fields
from .models import Item, Category, Subcategory

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
