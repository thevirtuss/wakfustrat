# Generated by Django 2.0.7 on 2018-08-18 11:27

from django.db import migrations, models
import wakfustrat.wiki.models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0007_auto_20180818_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=wakfustrat.wiki.models.upload_to_wiki_page_image, verbose_name='image'),
        ),
    ]
