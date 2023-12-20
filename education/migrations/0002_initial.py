# Generated by Django 4.2.4 on 2023-12-20 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='test',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.material', verbose_name='материал'),
        ),
        migrations.AddField(
            model_name='material',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.chapter', verbose_name='раздел'),
        ),
    ]
