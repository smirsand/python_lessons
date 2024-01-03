from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Класс нового пользователя.
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@test.ru',
            first_name='Test',
            last_name='Tests',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('12345')
        user.save()
