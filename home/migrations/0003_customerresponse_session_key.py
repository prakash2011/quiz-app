# Generated by Django 4.2.17 on 2024-12-27 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_customerresponse_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerresponse',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
