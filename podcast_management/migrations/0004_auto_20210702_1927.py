# Generated by Django 3.2.4 on 2021-07-02 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request_management', '0001_initial'),
        ('podcast_management', '0003_auto_20210702_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='podcast',
            name='id',
        ),
        migrations.AlterField(
            model_name='podcast',
            name='req',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='podcast', serialize=False, to='request_management.request'),
        ),
    ]
