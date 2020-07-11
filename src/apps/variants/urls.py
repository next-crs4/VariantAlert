# variants/url.py
from django.urls import path

from . import views


urlpatterns = [
    path('query/', views.Query.as_view(), name='query'),
    path('query/<query_id>', views.Details.as_view(), name='details'),
    path('query/<query_id>/rerun', views.Rerun.as_view(), name='rerun'),
    path('query/<query_id>/delete', views.Delete.as_view(), name='delete'),
    path('query/<query_id>/download', views.Download.as_view(), name='download'),
    path('history/', views.History.as_view(), name='history'),
]
