from django.shortcuts import render

# Create your views here.


def college_predictor_home(request):
    return render(request, 'collegepredictor/collegepredictor.html')