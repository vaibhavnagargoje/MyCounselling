from django.shortcuts import render

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    return render(request, 'landing_page/index.html')



def colleges(request):
    return render(request, 'landing_page/colleges.html')

def college_details(request):
    return render(request, 'landing_page/college-details.html')

def college_predictor(request):
    return render(request, 'landing_page/college-predictor.html')
def rank_predictor(request):
    return render(request, 'landing_page/rank-predictor.html')
def about_us(request):
    return render(request, 'landing_page/about-us.html')

def careers(request):
    return render(request,'landing_page/careers.html')