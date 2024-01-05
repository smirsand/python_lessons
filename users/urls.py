from users.views import LoginView, LogoutView, RegisterView, ProfileView, UserRetrieveAPIView
from django.urls import path

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-retrieve'),
]
