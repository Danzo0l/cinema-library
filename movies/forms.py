from django import forms

from .models import Reviews, RaitingStar, Raiting


class ReviewForm(forms.ModelForm):
    '''Review form'''

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class RaitingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RaitingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Raiting
        fields = ('star',)