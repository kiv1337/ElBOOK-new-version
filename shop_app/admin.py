from django.contrib import admin
from .models import Book, PurchaseRequest, Review, ForumPost, ForumTopic, Genre

class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_books', 'confirmed', 'rejected')

    def get_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])
    get_books.short_description = 'Books'

admin.site.register(Book)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(Review)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
admin.site.register(Genre)
