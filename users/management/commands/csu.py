from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Класс нового пользователя.
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@mail.ru',
            first_name='Sergey',
            last_name='Smirnov',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('12345')
        user.save()
