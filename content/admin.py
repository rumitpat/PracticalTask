from django.contrib import admin
from .models import Content, Suggestion, SharePost

# Register your models here.
admin.site.register(Content)
admin.site.register(Suggestion)
admin.site.register(SharePost)