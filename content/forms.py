from django import forms

from content.models import Content


class ContentAddFrom(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'summary']
