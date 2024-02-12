from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def second(response):
    return HttpResponse('<h2>Second page</h2>')
# Create your views here.
