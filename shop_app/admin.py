from django.contrib import admin
from .models import Book, PurchaseRequest, Cart, Review, ForumPost, ForumTopic, Genre

class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_books', 'confirmed', 'rejected')

    def get_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])
    get_books.short_description = 'Books'

    actions = ['confirm_requests', 'reject_requests']

    def confirm_requests(self, request, queryset):
        queryset.update(confirmed=True)
    confirm_requests.short_description = 'Подтвердить выбранные запросы'

    def reject_requests(self, request, queryset):
        for request in queryset:
            request.reject()
    reject_requests.short_description = 'Отклонить выбранные запросы'


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'has_books']

    def has_books(self, obj):
        return obj.books.exists()

    has_books.boolean = True
    has_books.short_description = 'Есть книги'
    
admin.site.register(Book)
admin.site.register(Cart, CartAdmin)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(Review)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
admin.site.register(Genre)
