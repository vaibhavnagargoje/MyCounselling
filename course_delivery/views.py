from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

from .models import CourseSession, CourseResource, StudentDeliverable
from products.models import MyProducts, UserSubscription


def get_user_enrolled_products(user):
    """
    Get all active products that a user is enrolled in via their subscriptions.
    """
    active_subscriptions = UserSubscription.objects.filter(
        user=user,
        status='active',
        is_active=True,
        expiry_date__gt=timezone.now()
    ).select_related('product')
    
    # Get unique products
    products = []
    seen_ids = set()
    for sub in active_subscriptions:
        if sub.product and sub.product.id not in seen_ids:
            products.append(sub.product)
            seen_ids.add(sub.product.id)
    
    return products


def get_sessions_for_user(user, product=None):
    """
    Get all sessions accessible to a user for a specific product or all enrolled products.
    Logic:
    - If is_public=True, anyone can see
    - If specific_users is populated, only those users can see
    - If specific_users is empty, all enrolled students can see
    """
    enrolled_products = get_user_enrolled_products(user)
    
    if product:
        if product not in enrolled_products:
            return CourseSession.objects.none()
        products_to_query = [product]
    else:
        products_to_query = enrolled_products
    
    # Get sessions that are:
    # 1. Public OR
    # 2. User is in specific_users OR
    # 3. No specific users set (available to all enrolled)
    sessions = CourseSession.objects.filter(
        Q(product__in=products_to_query) &
        (
            Q(is_public=True) |
            Q(specific_users=user) |
            Q(specific_users__isnull=True)
        )
    ).distinct().select_related('product').order_by('start_time')
    
    # Handle empty ManyToMany (no specific users = all enrolled can see)
    accessible_sessions = []
    for session in sessions:
        if session.is_public:
            accessible_sessions.append(session)
        elif session.specific_users.exists():
            if session.specific_users.filter(id=user.id).exists():
                accessible_sessions.append(session)
        else:
            # No specific users = available to all enrolled
            accessible_sessions.append(session)
    
    return accessible_sessions


def get_resources_for_user(user, product=None):
    """
    Get all resources accessible to a user for a specific product or all enrolled products.
    """
    enrolled_products = get_user_enrolled_products(user)
    
    if product:
        if product not in enrolled_products:
            return CourseResource.objects.none()
        products_to_query = [product]
    else:
        products_to_query = enrolled_products
    
    resources = CourseResource.objects.filter(
        Q(product__in=products_to_query) &
        (
            Q(is_public=True) |
            Q(specific_users=user) |
            Q(specific_users__isnull=True)
        )
    ).distinct().select_related('product').order_by('display_order', '-created_at')
    
    # Handle empty ManyToMany
    accessible_resources = []
    for resource in resources:
        if resource.is_public:
            accessible_resources.append(resource)
        elif resource.specific_users.exists():
            if resource.specific_users.filter(id=user.id).exists():
                accessible_resources.append(resource)
        else:
            accessible_resources.append(resource)
    
    return accessible_resources


def get_deliverables_for_user(user, product=None):
    """
    Get all student-specific deliverables for a user.
    """
    queryset = StudentDeliverable.objects.filter(student=user)
    
    if product:
        queryset = queryset.filter(product=product)
    
    return queryset.select_related('product', 'session').order_by('-created_at')


@login_required
def get_course_content_api(request, product_id=None):
    """
    API endpoint to fetch course content for dashboard.
    Returns JSON with sessions, resources, and deliverables.
    """
    user = request.user
    enrolled_products = get_user_enrolled_products(user)
    
    # Determine active product
    if product_id:
        product = get_object_or_404(MyProducts, id=product_id)
        if product not in enrolled_products:
            return JsonResponse({'error': 'Not enrolled in this course'}, status=403)
    else:
        product = enrolled_products[0] if enrolled_products else None
    
    now = timezone.now()
    
    # Get sessions for the product
    all_sessions = get_sessions_for_user(user, product)
    
    # Categorize sessions
    upcoming_sessions = [s for s in all_sessions if s.start_time > now][:5]
    live_sessions = [s for s in all_sessions if s.start_time <= now <= s.end_time]
    completed_sessions = [s for s in all_sessions if s.end_time < now and s.recording_url][:10]
    
    # Get resources
    resources = get_resources_for_user(user, product)
    
    # Get deliverables
    deliverables = get_deliverables_for_user(user, product)
    
    def serialize_session(session):
        return {
            'id': session.id,
            'title': session.title,
            'description': session.description,
            'start_time': session.start_time.isoformat(),
            'end_time': session.end_time.isoformat(),
            'platform': session.get_meeting_platform_display(),
            'meeting_link': session.meeting_link,
            'meeting_password': session.meeting_password,
            'recording_url': session.recording_url,
            'status': session.status,
            'product_name': session.product.name,
        }
    
    def serialize_resource(resource):
        return {
            'id': resource.id,
            'title': resource.title,
            'resource_type': resource.resource_type,
            'resource_type_display': resource.get_resource_type_display(),
            'content': resource.content,
            'video_url': resource.video_url,
            'file_url': resource.file_upload.url if resource.file_upload else None,
            'product_name': resource.product.name,
        }
    
    def serialize_deliverable(deliverable):
        return {
            'id': deliverable.id,
            'title': deliverable.title,
            'file_url': deliverable.file_upload.url if deliverable.file_upload else None,
            'remarks': deliverable.remarks,
            'created_at': deliverable.created_at.isoformat(),
            'product_name': deliverable.product.name,
        }
    
    data = {
        'enrolled_products': [
            {'id': p.id, 'name': p.name, 'slug': p.slug}
            for p in enrolled_products
        ],
        'active_product': {
            'id': product.id,
            'name': product.name,
            'slug': product.slug
        } if product else None,
        'live_sessions': [serialize_session(s) for s in live_sessions],
        'upcoming_sessions': [serialize_session(s) for s in upcoming_sessions],
        'completed_sessions': [serialize_session(s) for s in completed_sessions],
        'resources': [serialize_resource(r) for r in resources[:20]],
        'deliverables': [serialize_deliverable(d) for d in deliverables[:10]],
    }
    
    return JsonResponse(data)


@login_required
def session_detail(request, session_id):
    """
    View for individual session detail page.
    """
    user = request.user
    session = get_object_or_404(CourseSession, id=session_id)
    
    # Check access
    enrolled_products = get_user_enrolled_products(user)
    
    has_access = False
    if session.is_public:
        has_access = True
    elif session.product in enrolled_products:
        if session.specific_users.exists():
            has_access = session.specific_users.filter(id=user.id).exists()
        else:
            has_access = True
    
    if not has_access:
        return render(request, 'course_delivery/access_denied.html', status=403)
    
    context = {
        'session': session,
        'product': session.product,
    }
    return render(request, 'course_delivery/session_detail.html', context)


@login_required
def resource_detail(request, resource_id):
    """
    View for individual resource detail page.
    """
    user = request.user
    resource = get_object_or_404(CourseResource, id=resource_id)
    
    # Check access
    enrolled_products = get_user_enrolled_products(user)
    
    has_access = False
    if resource.is_public:
        has_access = True
    elif resource.product in enrolled_products:
        if resource.specific_users.exists():
            has_access = resource.specific_users.filter(id=user.id).exists()
        else:
            has_access = True
    
    if not has_access:
        return render(request, 'course_delivery/access_denied.html', status=403)
    
    context = {
        'resource': resource,
        'product': resource.product,
    }
    return render(request, 'course_delivery/resource_detail.html', context)
