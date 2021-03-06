# Generated by Django 4.0.2 on 2022-02-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(default='Unnamed', max_length=100)),
                ('ip_address', models.CharField(editable=False, max_length=100, null=True, verbose_name='IP address')),
                ('title', models.TextField(default='Untitled', verbose_name='title')),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], editable=False, max_length=50, null=True, verbose_name='severity')),
                ('cvss', models.FloatField(null=True)),
                ('publication_date', models.DateTimeField(null=True, verbose_name='publication date')),
                ('solved', models.BooleanField(default=False, verbose_name='solved')),
            ],
            options={
                'verbose_name': 'data',
                'verbose_name_plural': 'data',
                'db_table': 'data',
                'ordering': ['hostname', 'ip_address', 'title', 'severity'],
            },
        ),
    ]
