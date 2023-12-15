from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, ProfileForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy("users:login")


class LogoutView(BaseLogoutView):
    template_name = 'users/login.html'
    success_url = reverse_lazy("education:home")


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
