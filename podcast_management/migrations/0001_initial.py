# Generated by Django 3.2.4 on 2021-06-29 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('request_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='podcast')),
                ('delivery_date', models.DateField(null=True)),
                ('description', models.TextField(blank=True)),
                ('is_private', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=False)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='request_management.request')),
            ],
        ),
    ]
