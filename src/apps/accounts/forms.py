from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Type a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            msg = forms.ValidationError("This email address is already being used. "
                                        "Are you sure you are not already registered?")
            self.add_error('email', msg)

class UpdateForm(UserChangeForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Type a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')

    # def clean(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         msg = forms.ValidationError("This email address is already being used. "
    #                                     "Are you sure you are not already registered?")
    #         self.add_error('email', msg)
