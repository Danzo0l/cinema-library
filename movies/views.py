from django.shortcuts import render
from django.views.generic.base import View

from . import models

# Create your views here.
class MoviesView(View):
    '''Films list'''
    
    def get(self, request):
        movies = models.Movie.objects.all()
        data = {
            'movies_list': movies,
        }
        return render(request, 'movies/movie_list.html', context=data)