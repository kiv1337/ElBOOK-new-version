from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Book, Cart, PurchaseRequest, Genre, UserProfile, Review, ForumTopic, ForumPost
from django.db.models import Q, Avg
from django.http import HttpResponse
from .forms import AvatarForm, ReviewForm, ForumTopicForm, ForumPostForm, ChangeUsernameForm, ChangeEmailForm


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')
        return view_func(request, *args, **kwargs)
    return wrapper


def register(request):
    if request.user.is_authenticated:
        return HttpResponse("Вы уже вошли в аккаунт.")
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        if len(username) < 3:
            return render(request, 'registration/register.html', {'error_message': 'Имя пользователя должно содержать не менее 3 символов!'})
        
        if len(password) < 8:
            return render(request, 'registration/register.html', {'error_message': 'Пароль должен содержать не менее 8 символов!'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error_message': 'Имя пользователя уже используется!'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/register.html', {'error_message': 'Электронная почта уже используется!'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('profile')
    
    return render(request, 'registration/register.html')


def auth(request):
    if request.user.is_authenticated:
        return HttpResponse("Вы уже вошли в аккаунт.")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Неправильное имя пользователя или пароль.'})
    
    return render(request, 'registration/login.html')


def logOut(request):
    logout(request)
    return redirect(auth)


def catalog(request):
    query = request.GET.get('q')
    genre_filter = request.GET.get('genre')
    author_filter = request.GET.get('author')
    release_filter = request.GET.get('release')
    existing_genres = Genre.objects.all()
    existing_authors = Book.objects.values('author').distinct()

    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    if genre_filter and genre_filter != "":
        books = books.filter(genres__name=genre_filter)

    if author_filter:
        books = books.filter(author=author_filter)

    if release_filter == 'old':
        books = books.order_by('release_date')
    elif release_filter == 'new':
        books = books.order_by('-release_date')

    return render(request, 'catalog.html', {'books': books, 'query': query, 'existing_genres': existing_genres, 'existing_authors': existing_authors})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    average_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
    if average_rating is None:
        average_rating = "-"
    else:
        average_rating = round(average_rating, 1)
    return render(request, 'book_detail.html', {'book': book, 'average_rating': average_rating})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if PurchaseRequest.objects.filter(user=user, books=book, confirmed=True).exists():
        return redirect('book_detail', book_id=book.id)

    cart, created = Cart.objects.get_or_create(user=user)

    if book not in cart.books.all():
        cart.books.add(book)
        cart.save()

    return redirect('book_detail', book_id=book.id)

@login_required
def buy_now(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if PurchaseRequest.objects.filter(user=user, books=book, confirmed=True).exists():
        return redirect('catalog')

    purchase_request = PurchaseRequest.objects.create(user=user, confirmed=False)
    purchase_request.books.add(book)
    purchase_request.save()

    return redirect('profile')


@login_required
def remove_from_cart(request, book_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    book = get_object_or_404(Book, id=book_id)
    
    if book in cart.books.all():
        cart.books.remove(book)
        cart.save()
    
    return redirect('cart')

@login_required
def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        books_in_cart = cart.books.all()
        total_cost = cart.total_cost()
        cart_count = books_in_cart.count()
    except Cart.DoesNotExist:
        books_in_cart = []
        total_cost = 0
        cart_count = 0

    return render(request, 'cart.html', {'books_in_cart': books_in_cart, 'total_cost': total_cost, 'cart_count': cart_count})


@login_required
def purchase(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        
        if cart.books.exists():
            purchase_request = PurchaseRequest.objects.create(user=user, confirmed=False)
            purchase_request.books.set(cart.books.all())
            cart.books.clear()

        return redirect('profile')

    return redirect('cart')


@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    confirmed_purchases = PurchaseRequest.objects.filter(user=user, confirmed=True)

    purchased_books = []
    for purchase in confirmed_purchases:
        purchased_books.extend(purchase.books.all())
    
    purchased_books_count = len(purchased_books)

    if request.method == 'POST':
        avatar_form = AvatarForm(request.POST, request.FILES, instance=profile)
        if avatar_form.is_valid():
            avatar_form.save()
            return redirect('profile')
    else:
        avatar_form = AvatarForm(instance=profile)

    return render(request, 'profile.html', {
        'user': user, 
        'avatar_form': avatar_form, 
        'confirmed_purchases': purchased_books, 
        'purchased_books_count': purchased_books_count
    })


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if Review.objects.filter(user=request.user, book=book).exists():
        return render(request, 'book_detail.html', {'book': book, 'error_message': 'Нельзя оставлять несколько отзывов на одну книгу!'})

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()
    
    return render(request, 'book_detail.html', {'book': book, 'review_form': form})


def forum_view(request):
    topics = ForumTopic.objects.all()
    теги = ForumTopic.objects.values_list('тег', flat=True).distinct()
    тег_filter = request.GET.get('тег', '')
    return render(request, 'forum.html', {'topics': topics, 'теги': теги, 'тег_filter': тег_filter})


@login_required
def create_topic_view(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.creator = request.user
            topic.save()
            return redirect('forum')
    else:
        form = ForumTopicForm()
    return render(request, 'create_topic.html', {'form': form})


@login_required
def topic_detail_view(request, topic_id):
    topic = ForumTopic.objects.get(pk=topic_id)
    posts = ForumPost.objects.filter(topic=topic)
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('topic_detail', topic_id=topic_id)
    else:
        form = ForumPostForm()
    return render(request, 'topic_detail.html', {'topic': topic, 'posts': posts, 'form': form})


def contact(request):
    return render(request, 'contact.html')


def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            if User.objects.filter(username=new_username).exists():
                return render(request, 'change_username.html', {'form': form, 'error_message': 'Это имя пользователя уже используется.'})
            else:
                request.user.username = new_username
                request.user.save()
                return redirect('profile')
    else:
        form = ChangeUsernameForm()
    return render(request, 'change_username.html', {'form': form})


def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            if User.objects.filter(email=new_email).exists():
                return render(request, 'change_email.html', {'form': form, 'error_message': 'Этот email уже используется.'})
            else:
                request.user.email = new_email
                request.user.save()
                return redirect('profile')
    else:
        form = ChangeEmailForm()
    return render(request, 'change_email.html', {'form': form})