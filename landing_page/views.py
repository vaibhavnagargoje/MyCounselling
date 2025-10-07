from django.shortcuts import render

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    return render(request, 'landing_page/index.html')
