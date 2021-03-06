# Generated by Django 2.0.7 on 2018-08-04 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='nom')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('publish_date', models.DateTimeField(blank=True, null=True, verbose_name='date et heure de publication')),
                ('description', models.CharField(max_length=512, verbose_name='description/accroche')),
                ('markdown', models.TextField(verbose_name='markdown')),
                ('html', models.TextField(verbose_name='HTML')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='auteur')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
    ]
