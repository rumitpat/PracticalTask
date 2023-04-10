from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Profile

GENRE_CHOICES = [
    ('Blogging', 'Blogging'),
    ('News and Journalism', 'News and Journalism'),
    ('Creative Writing', 'Creative Writing'),
    ('Technical Writing', 'Technical Writing'),
    ('Copywriting', 'Copywriting'),
    ('Academic Writing', 'Academic Writing'),
    ('Travel Writing', 'Travel Writing'),
    ('Opinion Writing', 'Opinion Writing'),
]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    genre = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.Select(attrs={'class': 'genre-select'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        profile = Profile(user=user, genre=self.cleaned_data['genre'])
        profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
