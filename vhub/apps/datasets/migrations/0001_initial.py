# Generated by Django 4.0.2 on 2022-02-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datasets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unnamed', max_length=100)),
                ('file', models.FileField(upload_to='datasets', verbose_name='file')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'datasets',
                'verbose_name_plural': 'datasets',
                'db_table': 'datasets',
                'ordering': ['created_at', 'name'],
            },
        ),
    ]
