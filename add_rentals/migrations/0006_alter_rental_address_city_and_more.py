# Generated by Django 4.2.6 on 2024-01-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_rentals', '0005_remove_rental_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='address_city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='rental',
            name='address_street',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='rental',
            name='description',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='rental',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
