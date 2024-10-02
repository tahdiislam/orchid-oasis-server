# Generated by Django 5.0.6 on 2024-10-02 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flower',
            name='image',
        ),
        migrations.AddField(
            model_name='flower',
            name='image_url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
