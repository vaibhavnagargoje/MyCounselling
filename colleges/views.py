from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import EngineeringCollege, PlacementRecord

# Create your views here.

def colleges_list(request):
    """View to display list of colleges with search functionality"""
    search_query = request.GET.get('search', '')
    colleges_list = EngineeringCollege.objects.filter(is_active=True).select_related()
    
    if search_query:
        colleges_list = colleges_list.filter(
            Q(college_name__icontains=search_query) |
            Q(college_code__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(state__icontains=search_query)
        )
    
    # Order by ranking (null values last) and name
    colleges_list = colleges_list.order_by('nirf_ranking', 'college_name')
    
    context = {
        'colleges': colleges_list,
        'search_query': search_query,
        'total_colleges': colleges_list.count()
    }
    return render(request, 'colleges/colleges_list.html', context)

def college_detail(request, college_id):
    """View to display detailed information about a specific college"""
    college = get_object_or_404(EngineeringCollege, id=college_id, is_active=True)
    placement_records = PlacementRecord.objects.filter(
        college=college, 
        is_verified=True
    ).order_by('-academic_year')[:5]  # Latest 5 records
    
    context = {
        'college': college,
        'placement_records': placement_records,
    }
    return render(request, 'colleges/college_detail.html', context)