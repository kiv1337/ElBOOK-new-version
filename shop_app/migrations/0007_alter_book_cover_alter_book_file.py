# Generated by Django 4.2.2 on 2024-01-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0006_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to='covers/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(null=True, upload_to='books/'),
        ),
    ]
