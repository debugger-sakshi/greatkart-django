from .models import CartItem, Cart
from .views import _cart_id
def counter(request):
    cunt = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            for cart_item in cart_items:
                cunt += cart_item.quamtity
        except Cart.DoesNotExist:
            cunt = 0

    return dict(cart_count=cunt)

