# Generated by Django 2.0.7 on 2018-08-05 10:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import wakfustrat.wiki.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='nom')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='slug')),
                ('status', model_utils.fields.StatusField(choices=[('empty', 'Vide'), ('draft', 'Brouillon'), ('published', 'Terminé')], default='empty', max_length=100, no_check_for_status=True)),
                ('boss', models.CharField(max_length=64, verbose_name='boss')),
                ('level', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(200)], verbose_name='niveau')),
                ('difficulty', models.PositiveSmallIntegerField(choices=[(0, 'Très facile'), (1, 'Facile'), (2, 'Normal'), (3, 'Difficile'), (4, 'Très difficile')], help_text="Il s'agit d'une indication subjective à propos de la complexité de la stratégie du donjon", verbose_name='difficulté')),
                ('image', models.ImageField(blank=True, null=True, upload_to=wakfustrat.wiki.models.upload_to_wiki_page_image, verbose_name='image')),
                ('subzone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.SubZone', verbose_name='sous-zone')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Zone', verbose_name='zone')),
            ],
            options={
                'verbose_name': 'Boss ultime',
                'verbose_name_plural': 'Boss ultimes',
            },
        ),
    ]
