# Generated by Django 4.2.2 on 2024-05-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0029_remove_book_genres_book_genre_delete_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='shop_app.genre', verbose_name='Жанры'),
        ),
    ]
