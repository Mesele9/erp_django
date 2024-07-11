from django import forms
from .models import Category, Subcategory, Supplier, Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem
from django.forms.models import inlineformset_factory
from employee_management.models import Department

class DateInput(forms.DateInput):
    input_type = 'date'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone_number', 'address', 'tin_number']


class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select Category', required=True)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(), empty_label='Select Subcategory', required=False)

    class Meta:
        model = Item
        fields = ['description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty SubCategory queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')


class PurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        fields = ['date', 'supplier', 'purchaser', 'voucher_number', 'upload_receipt']
        widgets = {
            'date': DateInput(),
        }


class PurchaseRecordItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecordItem
        fields = ['item', 'quantity', 'unit_price']
        widgets = {
            'unit_price': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'class': 'item-select select2'})
        self.fields['item'].queryset = Item.objects.all()


class IssueRecordForm(forms.ModelForm):
    class Meta:
        model = IssueRecord
        fields = ['date', 'department', 'issued_by', 'received_by', 'voucher_number']
        widgets = {
            'date': DateInput(),
        }


class IssueRecordItemForm(forms.ModelForm):
    class Meta:
        model = IssueRecordItem
        fields = ['item', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'class': 'item-select select2'})
        self.fields['item'].queryset = Item.objects.all()


PurchaseRecordItemFormSet = inlineformset_factory(
    PurchaseRecord, PurchaseRecordItem, form=PurchaseRecordItemForm, extra=1, can_delete=True
)

IssueRecordItemFormSet = inlineformset_factory(
    IssueRecord, IssueRecordItem, form=IssueRecordItemForm, extra=1, can_delete=True
)


class ItemFilterForm(forms.Form):
    description = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label=False,
        empty_label='Select Category',
        widget=forms.Select(attrs={'placeholder': 'Category'}))
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(), required=False, label=False,
        empty_label='Select Subcategory', 
        widget=forms.Select(attrs={'placeholder': 'Subcategory'}))
    
    def __init__(self, *args, **kwargs):
        super(ItemFilterForm, self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass


class PurchaseRecordFilterForm(forms.Form):
    date_from = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    voucher_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Voucher Number'}))

class IssueRecordFilterForm(forms.Form):
    date_from = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    voucher_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Voucher Number'}))

class SupplierFilterForm(forms.Form):
    name = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Supplier Name'}))
    tin_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Tin Number'}))

class ReportForm(forms.Form):
    TRANSACTION_CHOICES = [
        ('', 'All'),
        ('purchase', 'Purchase'),
        ('issue', 'Issue'),
    ]

    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label='Transaction Type', required=False)
    department = forms.CharField(max_length=100, label='Department', required=False)
    supplier = forms.CharField(max_length=255, label='Supplier', required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data

class PurchaseReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    purchaser = forms.CharField(max_length=100, label='Purchaser', required=False)
    supplier = forms.CharField(max_length=255, label='Supplier', required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data

class IssueReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    department = forms.CharField(max_length=100, label='Department', required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data


class ItemsPurchasedReportForm(forms.Form):
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    voucher_number = forms.CharField(required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)
    description = forms.CharField(required=False)

class ItemsIssuedReportForm(forms.Form):
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    voucher_number = forms.CharField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    description = forms.CharField(required=False)


class SummarizedItemsPurchasedReportForm(forms.Form):
    date_from = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)

class SummarizedItemsIssuedReportForm(forms.Form):
    date_from = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)

