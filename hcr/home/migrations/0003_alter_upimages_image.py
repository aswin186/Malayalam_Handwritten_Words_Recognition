# Generated by Django 5.0.3 on 2024-04-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_upimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upimages',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
