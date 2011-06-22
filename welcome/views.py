# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'welcome/index.html', {'greeting': 'Sam'})