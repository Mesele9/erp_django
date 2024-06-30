from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import DecimalField, FloatField
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Sum, Q, Avg
from .models import Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem, Subcategory, Supplier
from .forms import IssueRecordFilterForm, IssueReportForm, ItemForm, ItemFilterForm, ItemsIssuedReportForm, ItemsPurchasedReportForm, PurchaseRecordFilterForm, PurchaseRecordForm, PurchaseRecordItemFormSet, IssueRecordForm, IssueRecordItemFormSet, PurchaseReportForm, ReportForm, SupplierForm, SupplierFilterForm


@login_required
def store_dashboard(request):
    #items = Item.objects.all()
    recent_purchase_records = PurchaseRecord.objects.order_by('-date')[:5]
    recent_issue_records = IssueRecord.objects.order_by('-date')[:5]
    low_stock_items = Item.objects.filter(stock_balance__lt=F('minimum_stock'))
    
    context = {
        #'items': items,
        'recent_purchase_records': recent_purchase_records,
        'recent_issue_records': recent_issue_records,
        'low_stock_items': low_stock_items,
    }
    
    return render(request, 'store/dashboard.html', context)

def get_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


@login_required
def supplier_list(request):
    form = SupplierFilterForm(request.GET or None)
    suppliers = Supplier.objects.all()

    if form.is_valid():
        if form.cleaned_data['name']:
            suppliers = suppliers.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['tin_number']:
            suppliers = suppliers.filter(tin_number=form.cleaned_data['tin_number'])

    return render(request, 'store/supplier_list.html', {'suppliers': suppliers, 'form': form})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'store/supplier_form.html', {'form': form})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'store/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'store/supplier_confirm_delete.html', {'supplier': supplier})

@login_required
def item_list(request):
    form = ItemFilterForm(request.GET or None)
    items = Item.objects.all()

    if form.is_valid():
        if form.cleaned_data['description']:
            items = items.filter(description__icontains=form.cleaned_data['description'])
        if form.cleaned_data['category']:
            items = items.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['subcategory']:
            items = items.filter(subcategory=form.cleaned_data['subcategory'])

    return render(request, 'store/item_list.html', {'items': items, 'form': form})


def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'store/item_form.html', {'form': form})

def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'store/item_form.html', {'form': form})

def item_delete(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'store/item_confirm_delete.html', {'item': item})


def purchase_record_list(request):
    form = PurchaseRecordFilterForm(request.GET or None)
    purchase_records = PurchaseRecord.objects.all()
    for p in purchase_records:
        print(p.total_value)

    if form.is_valid():
        if form.cleaned_data['voucher_number']:
            purchase_records = purchase_records.filter(voucher_number__icontains=form.cleaned_data['voucher_number'])

    return render(request, 'store/purchase_record_list.html', {'purchase_records': purchase_records, 'form': form})


def purchase_record_detail(request, pk):
    purchase_record = get_object_or_404(PurchaseRecord, pk=pk)
    purchase_record_items = PurchaseRecordItem.objects.filter(purchase_record=purchase_record)
    return render(request, 'store/purchase_record_detail.html', {'purchase_record': purchase_record, 'purchase_record_items': purchase_record_items})


def purchase_record_create(request):
    if request.method == 'POST':
        form = PurchaseRecordForm(request.POST, request.FILES)
        formset = PurchaseRecordItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase_record = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.purchase_record = purchase_record
                item.save()
            return redirect('purchase_record_list')
    else:
        form = PurchaseRecordForm()
        formset = PurchaseRecordItemFormSet()

    return render(request, 'store/purchase_record_form.html', {'form': form, 'formset': formset})


def purchase_record_edit(request, pk):
    purchase_record = get_object_or_404(PurchaseRecord, pk=pk)
    if request.method == 'POST':
        form = PurchaseRecordForm(request.POST, request.FILES, instance=purchase_record)
        formset = PurchaseRecordItemFormSet(request.POST, instance=purchase_record)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('purchase_record_list')
    else:
        form = PurchaseRecordForm(instance=purchase_record)
        formset = PurchaseRecordItemFormSet(instance=purchase_record)
    return render(request, 'store/purchase_record_form.html', {'form': form, 'formset': formset})


def purchase_record_delete(request, pk):
    purchase_record = get_object_or_404(PurchaseRecord, pk=pk)
    if request.method == 'POST':
        purchase_record.delete()
        return redirect('purchase_record_list')
    return render(request, 'store/purchase_record_confirm_delete.html', {'purchase_record': purchase_record})


def issue_record_list(request):
    form = IssueRecordFilterForm(request.GET or None)
    issue_records = IssueRecord.objects.all()

    if form.is_valid():
        if form.cleaned_data['voucher_number']:
            issue_records = issue_records.filter(voucher_number__icontains=form.cleaned_data['voucher_number'])

    return render(request, 'store/issue_record_list.html', {'issue_records': issue_records, 'form': form})


def issue_record_detail(request, pk):
    issue_record = get_object_or_404(IssueRecord, pk=pk)
    issue_record_items = IssueRecordItem.objects.filter(issue_record=issue_record)
    return render(request, 'store/issue_record_detail.html', {'issue_record': issue_record, 'issue_record_items': issue_record_items})


def issue_record_create(request):
    if request.method == 'POST':
        form = IssueRecordForm(request.POST)
        formset = IssueRecordItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            issue_record = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.issue_record = issue_record
                item.save()
            return redirect('issue_record_list')
    else:
        form = IssueRecordForm()
        formset = IssueRecordItemFormSet()

    return render(request, 'store/issue_record_form.html', {'form': form, 'formset': formset})


def issue_record_edit(request, pk):
    issue_record = get_object_or_404(IssueRecord, pk=pk)
    if request.method == 'POST':
        form = IssueRecordForm(request.POST, instance=issue_record)
        formset = IssueRecordItemFormSet(request.POST, instance=issue_record)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('issue_record_list')
    else:
        form = IssueRecordForm(instance=issue_record)
        formset = IssueRecordItemFormSet(instance=issue_record)
    return render(request, 'store/issue_record_form.html', {'form': form, 'formset': formset})


def issue_record_delete(request, pk):
    issue_record = get_object_or_404(IssueRecord, pk=pk)
    if request.method == 'POST':
        issue_record.delete()
        return redirect('issue_record_list')
    return render(request, 'store/issue_record_confirm_delete.html', {'issue_record': issue_record})


def generate_report(request):
    form = ReportForm(request.GET or None)
    report_data = []

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        transaction_type = form.cleaned_data['transaction_type']
        department = form.cleaned_data['department']
        supplier = form.cleaned_data['supplier']

        # Prepare filters based on form input
        filters = Q(date__gte=start_date, date__lte=end_date)

        if transaction_type:
            filters &= Q()  # Add filter for transaction type (purchase or issue)

        if department:
            filters &= Q()  # Add filter for department

        if supplier:
            filters &= Q()  # Add filter for supplier

        # Query database based on filters
        if transaction_type == 'purchase' or not transaction_type:
            purchase_records = PurchaseRecord.objects.filter(filters).order_by('date')
            report_data.extend(purchase_records)

        if transaction_type == 'issue' or not transaction_type:
            issue_records = IssueRecord.objects.filter(filters).order_by('date')
            report_data.extend(issue_records)

    context = {
        'form': form,
        'report_data': report_data,
    }
    for r in report_data:
        print(r)

    return render(request, 'store/report.html', context)

def purchase_report(request):
    form = PurchaseReportForm(request.GET or None)
    report_data = []

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        purchaser = form.cleaned_data['purchaser']
        supplier = form.cleaned_data['supplier']

        filters = Q(date__gte=start_date, date__lte=end_date)
        if purchaser:
            filters &= Q(purchaser=purchaser)
        if supplier:
            filters &= Q(supplier__name=supplier)

        purchase_records = PurchaseRecord.objects.filter(filters).order_by('date')
        report_data.extend(purchase_records)

    context = {
        'form': form,
        'report_data': report_data,
    }

    return render(request, 'store/purchase_report.html', context)

def issue_report(request):
    form = IssueReportForm(request.GET or None)
    report_data = []

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        department = form.cleaned_data['department']

        filters = Q(date__gte=start_date, date__lte=end_date)
        if department:
            filters &= Q(department=department)

        issue_records = IssueRecord.objects.filter(filters).order_by('date')
        report_data.extend(issue_records)

    context = {
        'form': form,
        'report_data': report_data,
    }

    return render(request, 'store/issue_report.html', context)



def purchase_items_report(request):
    form = PurchaseReportForm(request.GET or None)
    report_data = []

    if request.method == 'GET' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        purchaser = form.cleaned_data['purchaser']
        supplier = form.cleaned_data['supplier']

        # Aggregate total quantities for each item
        purchase_items = PurchaseRecordItem.objects.filter(purchase_record__date__range=(start_date, end_date))
        if purchaser:
            purchase_items = purchase_items.filter(purchase_record__purchaser=purchaser)
        if supplier:
            purchase_items = purchase_items.filter(purchase_record__supplier=supplier)

        aggregated_data = purchase_items.values('item__description').annotate(
            total_quantity=Sum('quantity'),
            average_price=Avg('unit_price'),
            total_value=Sum('quantity') * Avg('unit_price')
        )

        for item_data in aggregated_data:
            
            item_description = item_data['item__description']
            total_quantity = item_data['total_quantity']
            total_value = item_data['total_value']
            report_data.append({
                
                'item_description': item_description,
                'total_quantity': total_quantity,
                'total_value': total_value
            })

    context = {
        'form': form,
        'report_data': report_data,
    }
    return render(request, 'store/purchase_items_report.html', context)


def issue_items_report(request):
    form = IssueReportForm(request.GET or None)
    report_data = []

    if request.method == 'GET' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        department = form.cleaned_data['department']

        # Aggregate total quantities for each item
        issue_items = IssueRecordItem.objects.filter(issue_record__date__range=(start_date, end_date))
        if department:
            issue_items = issue_items.filter(issue_record__department=department)

        aggregated_data = issue_items.values('item__description').annotate(
            total_quantity=Sum('quantity'),
            average_price=Avg('unit_price'),
            total_value=Sum('quantity') * Avg('unit_price')
        )

        for item_data in aggregated_data:
            item_description = item_data['item__description']
            total_quantity = item_data['total_quantity']
            total_value = item_data['total_value']
            report_data.append({
                'item_description': item_description,
                'total_quantity': total_quantity,
                'total_value': total_value
            })

    context = {
        'form': form,
        'report_data': report_data,
    }
    return render(request, 'store/issue_items_report.html', context)
