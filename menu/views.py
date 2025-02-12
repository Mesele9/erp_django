from django.shortcuts import render, get_object_or_404
from .models import MainCategory, Category, MenuItem, Rating
from .forms import RatingForm
import qrcode
from django.http import HttpResponse
from django.conf import settings
import os
from django.db.models import Q


def menu_view(request):
    main_categories = MainCategory.objects.all()
    
    # Default to "Restaurant" if exists, else first main category
    default_main_category = MainCategory.objects.filter(name="Restaurant").first()
    if not default_main_category and main_categories.exists():
        default_main_category = main_categories.first()
    
    # Get selected main category
    selected_main_category_id = request.GET.get('main_category')
    if selected_main_category_id:
        selected_main_category = get_object_or_404(MainCategory, id=selected_main_category_id)
    elif default_main_category:
        selected_main_category = default_main_category
    else:
        selected_main_category = None
    
    # Get parameters
    selected_subcategory = request.GET.get('subcategory')
    search_query = request.GET.get('search', '')
    
    # Get subcategories
    subcategories = Category.objects.filter(main_category=selected_main_category) if selected_main_category else []
    
    # Base queryset
    menu_items = MenuItem.objects.none()

    if selected_main_category:
        # Get all subcategory IDs for the main category
        subcategory_ids = subcategories.values_list('id', flat=True)
        
        if selected_subcategory or search_query:
            # Start with items in the main category
            menu_items = MenuItem.objects.filter(
                categories__id__in=subcategory_ids,
                is_active=True
            ).distinct()
            
            # Apply subcategory filter if selected
            if selected_subcategory:
                menu_items = menu_items.filter(categories__id=selected_subcategory)
            
            # Apply search filter if query exists
            if search_query:
                menu_items = menu_items.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query)
                ).distinct()

    context = {
        'main_categories': main_categories,
        'selected_main_category': selected_main_category,
        'subcategories': subcategories,
        'menu_items': menu_items,
        'selected_subcategory': selected_subcategory,
        'search_query': search_query
    }
    return render(request, 'menu/menu.html', context)


def menu_item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    ratings = Rating.objects.filter(menu_item=item)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.create(
                menu_item=item,
                stars=form.cleaned_data['stars'],
                comment=form.cleaned_data['comment'],
                guest_name=form.cleaned_data['guest_name']
            )
    else:
        form = RatingForm()

    context = {
        'item': item,
        'ratings': ratings,
        'form': form
    }
    return render(request, 'menu/detail.html', context)
