from django.shortcuts import render

# Create your views here.


def rank_predictor_home(request):
    return render(request, 'rankpredictor/rankpredictor.html')