from django.shortcuts import render
from django.http import HttpResponse

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

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

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


def statistics_view(request):
    matplotlib.use('Agg')
    from django.db.models import Count
    from collections import Counter

    data_year = Movie.objects.values('year').annotate(total=Count('year')).order_by('year')

    years = [item['year'] if item['year'] else "None" for item in data_year]
    totals_year = [item['total'] for item in data_year]

    plt.figure()
    plt.bar(range(len(years)), totals_year)
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(years)), years, rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()

    graphic_year = base64.b64encode(buffer_year.getvalue()).decode()
    buffer_year.close()

    
    all_movies = Movie.objects.all()
    genre_counter = Counter()

    for movie in all_movies:
        if movie.genre:
            genres = movie.genre.split(',')
            for g in genres:
                genre_counter[g.strip()] += 1

  
    top_genres = genre_counter.most_common(10)

    genres = [item[0] for item in top_genres]
    totals_genre = [item[1] for item in top_genres]

    plt.figure()
    plt.bar(range(len(genres)), totals_genre)
    plt.title('Top 10 Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(genres)), genres, rotation=45)
    plt.subplots_adjust(bottom=0.3)

    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    graphic_genre = base64.b64encode(buffer_genre.getvalue()).decode()
    buffer_genre.close()

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })