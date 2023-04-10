from django.urls import path
from .views import ContentListView, about, add_content, ContentDetailView, update_content, ContentDeleteView, \
    ContentDraftListView, search_content, ReceiveContentListView, receive_content

urlpatterns = [
    path('', ContentListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('content/new/', add_content, name='content-create'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='content-detail'),
    path('content/<int:pk>/update', update_content, name='content-update'),
    path('content/<int:pk>/delete', ContentDeleteView.as_view(), name='content-delete'),
    path('draft/', ContentDraftListView.as_view(), name='content-draft'),
    path('content/search/<int:pk>/', search_content, name='content-search'),
    path('content/received/', receive_content, name='content-received'),
]
