# variants/url.py
from django.urls import path

from . import views


urlpatterns = [
    path('query/', views.Query.as_view(), name='query'),
    path('query/<query_id>', views.Details.as_view(), name='details'),
    path('query/<query_id>/rerun', views.Rerun.as_view(), name='rerun'),
    path('history/', views.History.as_view(), name='history'),
]
