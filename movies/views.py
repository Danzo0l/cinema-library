from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from . import models
from . import forms


# Create your views here.
class MoviesView(ListView):
    '''Films list'''
    
    model = models.Movie
    queryset = models.Movie.objects.filter(draft=False)
    # template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
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