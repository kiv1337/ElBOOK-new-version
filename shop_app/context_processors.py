from .models import Cart

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.books.count()
        except Cart.DoesNotExist:
            pass
    return {'cart_count': cart_count}
