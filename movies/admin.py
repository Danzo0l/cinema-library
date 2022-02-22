from django.contrib import admin
from django.utils.safestring import mark_safe

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


from .models import *
# Register your models here.


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'url')
    list_display_links = ('name', 'id')


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    fields = ('title', 'get_image', )
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="120px">')

    get_image.short_description = 'Image'


@admin.register(Movie)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'title')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInline, ]
    save_on_top = True
    save_as = True
    readonly_fields = ('get_image', 'draft')
    form = MovieAdminForm
    actions = ['publish', 'unpublish']

    fieldsets = (
            ('Main info', {
                'fields': (('title', 'tagline'), )
            }),
            ('View info', {
                'fields': (('description', 'get_image'),)
            }),
            ('Premiere', {
                'fields': (('year', 'world_premiere', 'country'),)
            }),
            ('Actors and directors', {
                'classes': ('collapse',),
                'fields': (('actors', 'directors', 'genres', 'category'),)
            }),
            ('Finance', {
                'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
            }),
            ('URL configuration', {
                'fields': (('url', 'draft'),)
            }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" height="220px">')

    def unpublish(self, request, queryset):
        '''unpin from publication'''
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записаей обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Go publication'''
        row_update = queryset.update(draft=False)
        if row_update == '1':
            message_bit = '1 updating'
        else:
            message_bit = f'{row_update} записаей обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'publish'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'unpublish'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Image'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')

    #сокрытие поля для редактирования
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="60px">')

    get_image.short_description = 'Image'


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'get_image')
    list_editable = ('status',)
    list_filter = ('status', 'name')
    search_fields = ('name', )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="60px">')

    get_image.short_description = 'Image'


@admin.register(Raiting)
class RaitingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie')


admin.site.register(RaitingStar)

admin.site.site_title = 'Cinema-library'
admin.site.site_header = 'cinema-library'
