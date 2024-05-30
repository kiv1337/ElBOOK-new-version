from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField('Название', max_length=56)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField('Название', max_length=128)
    author = models.CharField('Автор', max_length=128)
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    cost = models.IntegerField('Цена')
    release_date = models.DateField('Дата выпуска')
    file = models.FileField(null=True, upload_to='books/')
    description = models.TextField('Описание', null=True)
    cover = models.ImageField('Обложка', upload_to='covers/', null=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
   

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField('Book')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def total_cost(self):
        return sum(book.cost for book in self.books.all())
    

class PurchaseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    confirmed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Запрос на покупку'
        verbose_name_plural = 'Запросы на покупку'

    def __str__(self):
        book_titles = ", ".join([book.title for book in self.books.all()])
        return f"{self.user.username} - {book_titles}"

    def reject(self):
        self.rejected = True
        self.save()

    def confirm(self):
        self.confirmed = True
        self.save()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ForumTopic(models.Model):
    название = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    тег = models.CharField(max_length=50) 
    
    class Meta:
        verbose_name = 'Топик на форуме'
        verbose_name_plural = 'Топики на форуме'

    def __str__(self):
        return self.название

class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    сообщение = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Сообщение на форуме'
        verbose_name_plural = 'Сообщения на форуме'

    def __str__(self):
        return f'{self.author.username} - {self.topic.название}'