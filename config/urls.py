from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('education.urls', namespace='education')),  # Переходит в приложение в файл urls.py
                  path('users/', include('users.urls', namespace='users')),  # Переходит в приложение в файл urls.py

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
