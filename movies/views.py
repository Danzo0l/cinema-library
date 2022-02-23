from django.db.models import Q
from django.http import JsonResponse, HttpResponse
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = forms.RaitingForm()
        return context


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
        return queryset


class JsonFilterMovieView(ListView):
    def get_queryset(self):
        queryset = models.Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
         ).distinct().values('title', 'tagline', 'url', 'poster')

        print(queryset)
        if str(queryset) == '<QuerySet []>':
            queryset = models.Movie.objects.all().distinct().values('title', 'tagline', 'url', 'poster')

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies': queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = forms.RaitingForm(request.POST)
        if form.is_valid():
            models.Raiting.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

