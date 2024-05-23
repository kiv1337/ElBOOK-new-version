from django.contrib import admin
from django.urls import path, include
from shop_app.views import register, auth, catalog, profile, logOut, book_detail, add_to_cart, cart, purchase, remove_from_cart, add_review, forum_view, create_topic_view, topic_detail_view, contact, change_email, change_username, buy_now
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', auth, name='auth'),
    path('', catalog, name='catalog'),
    path('profile/', profile, name='profile'),
    path('logout/', logOut, name='logout'),
    path('book_detail/<int:book_id>/', book_detail, name='book_detail'),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('purchase/', purchase, name='purchase'),
    path('cart/remove/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('add_review/<int:book_id>/', add_review, name='add_review'),
    path('forum/', forum_view, name='forum'),
    path('forum/create_topic/', create_topic_view, name='create_topic'),
    path('forum/topic/<int:topic_id>/', topic_detail_view, name='topic_detail'),
    path('contact/', contact, name='contact'),
    path('change_username/', change_username, name='change_username'),
    path('change_email/', change_email, name='change_email'),
    path('buy_now/<int:book_id>/', buy_now, name='buy_now'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
