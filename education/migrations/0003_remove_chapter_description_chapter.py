# Generated by Django 4.2.4 on 2023-12-15 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_rename_materials_material_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='description_chapter',
        ),
    ]
