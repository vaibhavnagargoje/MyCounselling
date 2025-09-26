from django.shortcuts import render

# Create your views here.

def colleges(request):
    return render(request, 'colleges/colleges.html')