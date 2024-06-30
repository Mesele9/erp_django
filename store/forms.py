from django import forms
from .models import Category, Subcategory, Supplier, Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem
from django.forms.models import inlineformset_factory

class DateInput(forms.DateInput):
    input_type = 'date'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone_number', 'address', 'tin_number']


class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select Category', required=True)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), empty_label='Select Subcategory', required=False)

    class Meta:
        model = Item
        fields = ['description', 'category', 'subcategory', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock']


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
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), required=False, label=False,
        empty_label='Select Subcategory', 
        widget=forms.Select(attrs={'placeholder': 'Subcategory'}))
    
class PurchaseRecordFilterForm(forms.Form):
    voucher_number = forms.CharField(required=False, label=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Voucher Number'}))

class IssueRecordFilterForm(forms.Form):
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
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    purchaser = forms.CharField(label='Purchaser', max_length=100, required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)


class ItemsIssuedReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')
    department = forms.CharField(label='Department')

class IssueItemReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    department = forms.CharField(required=False)
