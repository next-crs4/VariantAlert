# accounts/views.py
from . import forms
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
