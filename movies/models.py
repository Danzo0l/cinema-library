from django.db import models
import datetime
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    '''Категории. Модель для описания категорий фильмов'''

    name = models.CharField(max_length=150, verbose_name='name')
    description = models.TextField(verbose_name='description')
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    '''Актеры и режиссеры'''
    name = models.CharField(max_length=150, verbose_name='actor name')
    age = models.PositiveSmallIntegerField(default=0, verbose_name='ages')
    description = models.TextField(verbose_name='description')
    image = models.ImageField(upload_to='actors/', verbose_name='photo')
    status = models.BooleanField(default=0, verbose_name='is_director')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actors and directors'
        verbose_name_plural = 'Actors and directors'


class Genre(models.Model):
    '''Genres'''

    name = models.CharField(max_length=150, verbose_name='genre naming')
    description = models.TextField(verbose_name='description')
    url  =models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    '''Movie'''

    title = models.CharField(max_length=100, verbose_name='name')
    tagline = models.CharField(max_length=100, default='', verbose_name='tagline')
    description = models.TextField(verbose_name='description')
    poster = models.ImageField(upload_to='movies/', verbose_name='poster')
    year = models.PositiveSmallIntegerField(default=2019, verbose_name='start year')
    country = models.CharField(max_length=64, verbose_name='Country')
    directors = models.ManyToManyField(Actor, verbose_name='director', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='actors', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='genre')
    world_premiere = models.DateField(default=datetime.date.today, verbose_name='World premier')
    budget = models.PositiveIntegerField(default=0, help_text='budget (in USD)', verbose_name='Budget')
    fees_in_usa = models.PositiveIntegerField(default=0, help_text='fees in USA (USD)', verbose_name='Fees in USA')
    fees_in_world = models.PositiveIntegerField(default=0, help_text='fees in world (USD)', verbose_name='Fees in world')
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(verbose_name='It is draft', default=False)

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    '''Shots from Movie'''
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='description')
    image = models.ImageField(upload_to='movie_shots/', verbose_name='Image')
    movie = models.ForeignKey(Movie, verbose_name='from film', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'MovieShot'
        verbose_name_plural = 'MovieShots'


class RaitingStar(models.Model):
    '''Raiting'''

    value = models.PositiveSmallIntegerField(default=0, verbose_name='value')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Star'
        verbose_name_plural = 'Stars'


class Raiting(models.Model):
    '''Movie raiting'''
    ip = models.CharField(max_length=15, verbose_name='IP')
    star = models.ForeignKey(RaitingStar, on_delete=models.CASCADE, verbose_name='star')
    movie = models.ForeignKey(Movie, verbose_name='from movie', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Raiting'
        verbose_name_plural = 'Raitings'


class Reviews(models.Model):
    '''Reviews'''

    email = models.EmailField()
    name = models.CharField(max_length=100, verbose_name='name')
    text = models.TextField(max_length=2000)
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, verbose_name='movie', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
