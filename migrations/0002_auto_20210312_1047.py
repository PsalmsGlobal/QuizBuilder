# Generated by Django 3.1.6 on 2021-03-12 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='date_updated',
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(max_length=200),
        ),
    ]
