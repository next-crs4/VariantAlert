# accounts/views.py
from . import forms
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.models import User


class SignUp(generic.CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class Update(generic.UpdateView):
    form_class = forms.UpdateForm
    model = User
    success_url = reverse_lazy('history')
    template_name = 'accounts/update.html'


