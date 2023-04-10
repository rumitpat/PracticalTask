from django.urls import path
from .views import TwitterListView

urlpatterns = [
    path('', TwitterListView.as_view(), name='twitter-trends'),
]
