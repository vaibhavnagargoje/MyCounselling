from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyProducts, BundledPlan, ExamType, ProductCategory, Order

# Create your views here.
@login_required
def products_plans(request):
    # Fetch active filters
    exam_types = ExamType.objects.filter(is_active=True).order_by('display_order')
    categories = ProductCategory.objects.filter(is_active=True).order_by('display_order')
    
    # Fetch active items
    products = MyProducts.objects.filter(is_active=True).select_related('category', 'exam_type').order_by('display_order')
    bundles = BundledPlan.objects.filter(is_active=True).order_by('display_order')
    
    # Prepare featured items for carousel
    featured_items = []
    for plan in bundles.filter(is_featured=True):
        featured_items.append({
            'obj': plan,
            'type': 'Plan',
            'price': plan.selling_price,
            'original_price': plan.original_price,
            'discount': plan.discount_percentage
        })
    
    for prod in products.filter(is_featured=True):
        featured_items.append({
            'obj': prod,
            'type': 'Product',
            'price': prod.base_price,
            'original_price': None,
            'discount': 0
        })

    context = {
        'exam_types': exam_types,
        'categories': categories,
        'products': products,
        'bundles': bundles,
        'featured_items': featured_items,
    }
    return render(request, 'products/all_products.html', context)

@login_required
def product_detail(request, type, slug):
    context = {}
    
    if type == 'bundle':
        item = get_object_or_404(BundledPlan, slug=slug, is_active=True)
        # Get related bundles
        related_items = BundledPlan.objects.filter(is_active=True).exclude(id=item.id)[:3]
        context['is_bundle'] = True
    else:
        item = get_object_or_404(MyProducts, slug=slug, is_active=True)
        # Get related products in same category
        related_items = MyProducts.objects.filter(is_active=True).exclude(id=item.id)
        if item.category:
            related_items = related_items.filter(category=item.category)
        related_items = related_items[:3]
        context['is_bundle'] = False

    context.update({
        'item': item,
        'type': type,
        'related_items': related_items
    })
    return render(request, 'products/product_detail.html', context)

