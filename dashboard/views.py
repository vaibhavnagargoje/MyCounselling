from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from course_delivery.views import (
    get_user_enrolled_products,
    get_sessions_for_user,
    get_resources_for_user,
    get_deliverables_for_user
)
from products.models import MyProducts


@login_required(login_url='user:login')
def dashboard(request):
    """
    Main dashboard view that shows course content based on user's enrollments.
    Supports switching between enrolled courses via query parameter.
    """
    user = request.user
    
    # Get all enrolled products for the user
    enrolled_products = get_user_enrolled_products(user)
    
    # Determine which product to show (from query param or first enrolled)
    selected_product_id = request.GET.get('course')
    active_product = None
    
    if selected_product_id:
        try:
            active_product = next(
                (p for p in enrolled_products if str(p.id) == selected_product_id),
                None
            )
        except (ValueError, StopIteration):
            pass
    
    # Default to first enrolled product if none selected
    if not active_product and enrolled_products:
        active_product = enrolled_products[0]
    
    now = timezone.now()
    
    # Initialize empty data
    live_sessions = []
    upcoming_sessions = []
    completed_sessions = []
    resources = []
    deliverables = []
    
    if active_product:
        # Get sessions for the active product
        all_sessions = get_sessions_for_user(user, active_product)
        
        # Categorize sessions by status
        live_sessions = [s for s in all_sessions if s.start_time <= now <= s.end_time]
        upcoming_sessions = [s for s in all_sessions if s.start_time > now][:5]
        completed_sessions = [s for s in all_sessions if s.end_time < now and s.recording_url][:10]
        
        # Get resources and deliverables
        resources = get_resources_for_user(user, active_product)[:10]
        deliverables = get_deliverables_for_user(user, active_product)[:5]
    
    context = {
        'enrolled_products': enrolled_products,
        'active_product': active_product,
        'live_sessions': live_sessions,
        'upcoming_sessions': upcoming_sessions,
        'completed_sessions': completed_sessions,
        'resources': resources,
        'deliverables': deliverables,
        'has_enrollments': len(enrolled_products) > 0,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


