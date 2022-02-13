# Generated by Django 4.0.2 on 2022-02-12 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasets',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
