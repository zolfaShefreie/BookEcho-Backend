# Generated by Django 3.2.4 on 2021-07-05 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='book_title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
