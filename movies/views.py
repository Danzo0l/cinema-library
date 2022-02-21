from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from . import models


# Create your views here.
class MoviesView(ListView):
    '''Films list'''
    
    model = models.Movie
    queryset = models.Movie.objects.filter(draft=False)
    #template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
    '''full movie description'''

    model = models.Movie
    slug_field = 'url'

