# Generated by Django 4.2.2 on 2024-05-20 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0036_remove_purchaserequest_book_purchaserequest_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserequest',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
