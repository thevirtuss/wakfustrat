# Generated by Django 2.0.7 on 2018-08-04 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='server',
            field=models.CharField(blank=True, choices=[('DAT', 'Dathura'), ('AER', 'Aerafal'), ('REM', 'Remington'), ('ELB', 'Elbor'), ('NOX', 'Nox'), ('EFR', 'Efrim'), ('PHA', 'Phaeris')], max_length=20, null=True, verbose_name='serveur'),
        ),
    ]