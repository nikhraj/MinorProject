from django.shortcuts import render

# Create your views here.


def home_view(request):
    return render(request,'home.html')

def dashboard_view(request,ID):
    return render(request,'dashboard.html',{'user_id':ID})