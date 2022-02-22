from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from . import models
from . import forms


# Create your views here.
class GenreYear:

    def get_genres(self):
        return models.Genre.objects.all()

    def get_years(self):
        return models.Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    '''Films list'''
    
    model = models.Movie
    queryset = models.Movie.objects.filter(draft=False)


class MovieDetailView(GenreYear, DetailView):
    '''full movie description'''


    model = models.Movie
    slug_field = 'url'


class AddReview(View):
    '''Reviews'''

    def post(self, request, pk):
        form = forms.ReviewForm(request.POST)
        movie = models.Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = models.Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMovieView(GenreYear, ListView):

    def get_queryset(self):
        queryset = models.Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        )
        print(queryset)
        return queryset

