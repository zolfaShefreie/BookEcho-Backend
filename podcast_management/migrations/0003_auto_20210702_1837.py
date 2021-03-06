# Generated by Django 3.2.4 on 2021-07-02 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request_management', '0001_initial'),
        ('podcast_management', '0002_podcast_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='podcast',
            name='request',
        ),
        migrations.AddField(
            model_name='podcast',
            name='req',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='podcast', to='request_management.request'),
            preserve_default=False,
        ),
    ]
