from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

    #return HttpResponse("<h1>Welcome Homepage</h1>")
    #return render(request, "home.html")
    # return render(request, "home.html", {"name" : "Emily Cardona"})

def home(request):
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
   return HttpResponse("<h1>Welcome About</h1>")


# Create your views here.
