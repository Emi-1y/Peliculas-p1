from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    #return HttpResponse("<h1>Welcome Homepage</h1>")
    #return render(request, "home.html")
     return render(request, "home.html", {"name" : "Emily Cardona"})

def About(request):
    return HttpResponse("<h1>Welcome About</h1>")


# Create your views here.
