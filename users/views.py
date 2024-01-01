from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, ProfileForm
from users.models import User


class LoginView(BaseLoginView):
    """
    Класс для отображения страницы входа пользователя.
    """
    template_name = 'users/login.html'
    success_url = reverse_lazy("users:login")


class LogoutView(BaseLogoutView):
    """
    Класс для отображения страницы выхода пользователя.
    """
    template_name = 'users/login.html'
    success_url = reverse_lazy("education:home")


class RegisterView(CreateView):
    """
    Класс для отображения страницы регистрации пользователя.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Класс для отображения страницы профиля пользователя.
    """
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
