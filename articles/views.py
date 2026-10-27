from django.shortcuts import render
from django.http.response import HttpResponse   
# Create your views here.

def hello_world(request):
    return HttpResponse("<h1>Hello world</h1>")


def hello_name(request, name):
    return HttpResponse(f"Hello <h1>{name}</h1>")



#HOMEWORK
def info(request):
    return HttpResponse(f"Ваш браузер: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36.")