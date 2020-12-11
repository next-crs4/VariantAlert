# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('update/<slug:pk>', views.Update.as_view(), name='update_user'),
]
