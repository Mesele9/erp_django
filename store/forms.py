from django import forms
from crispy_forms.helper import FormHelper
from .models import Category, Subcategory, Supplier, Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem
from django.forms.models import inlineformset_factory
from employee_management.models import Department

class DateInput(forms.DateInput):
    input_type = 'date'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone_number', 'address', 'tin_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'tin_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SupplierFilterForm(forms.Form):
    name = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Supplier Name', 'class': 'form-control'}))
    tin_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Tin Number', 'class': 'form-control'}))

""" 
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone_number', 'address', 'tin_number']


class SupplierFilterForm(forms.Form):
    name = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Supplier Name'}))
    tin_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Tin Number'}))
 """


class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select Category', required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(), empty_label='Select Subcategory', required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Item
        fields = ['description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock']

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.Select(attrs={'class': 'form-control'}),
            'current_unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'minimum_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)


        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = Subcategory.objects.none()
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')


class ItemFilterForm(forms.Form):
    description = forms.CharField(required=False, label=False,
        widget=forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label=False,
        empty_label='Select Category',
        widget=forms.Select(attrs={'placeholder': 'Category', 'class': 'form-control'}))
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(), required=False, label=False,
        empty_label='Select Subcategory',
        widget=forms.Select(attrs={'placeholder': 'Subcategory', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ItemFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = Subcategory.objects.none()


class PurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        fields = ['date', 'supplier', 'purchaser', 'voucher_number', 'upload_receipt']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'purchaser': forms.TextInput(attrs={'class': 'form-control'}),
            'voucher_number': forms.TextInput(attrs={'class': 'form-control'}),
            'upload_receipt': forms.FileInput(attrs={'class': 'form-control'}),
        }


class PurchaseRecordItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecordItem
        fields = ['item', 'quantity', 'unit_price']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control item-select select2'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()


PurchaseRecordItemFormSet = inlineformset_factory(
    PurchaseRecord, PurchaseRecordItem, form=PurchaseRecordItemForm, extra=1, can_delete=True
)


class PurchaseRecordFilterForm(forms.Form):
    date_from = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    date_to = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    voucher_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Voucher Number', 'class': 'form-control'}))


class IssueRecordForm(forms.ModelForm):
    class Meta:
        model = IssueRecord
        fields = ['date', 'department', 'issued_by', 'received_by', 'voucher_number']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'issued_by': forms.TextInput(attrs={'class': 'form-control'}),
            'received_by': forms.TextInput(attrs={'class': 'form-control'}),
            'voucher_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IssueRecordItemForm(forms.ModelForm):
    class Meta:
        model = IssueRecordItem
        fields = ['item', 'quantity']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control item-select select2'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()


IssueRecordItemFormSet = inlineformset_factory(
    IssueRecord, IssueRecordItem, form=IssueRecordItemForm, extra=1, can_delete=True
)


class IssueRecordFilterForm(forms.Form):
    date_from = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    date_to = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    voucher_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Voucher Number', 'class': 'form-control'}))


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

