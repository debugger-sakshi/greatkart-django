from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_Cart(request,product_id):
    product = Product.objects.get(id = product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            # return HttpResponse(key+" "+ value)
            # exit()
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact= key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
        

    try:
        cart = Cart.objects.get(cart_id= _cart_id(request)) # get the cart using the cart id present in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product = product, cart = cart)


    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,  cart = cart)

        ex_variation_li = []
        ids = []
        for c in cart_item:
            ex_variation_li.append(list(c.variation.all()))
            ids.append(c.id)

        print(ex_variation_li)
        if product_variation in ex_variation_li:
            # increase  quantity
            index = ex_variation_li.index(product_variation)
            item = CartItem.objects.get(product=product, id=ids[index])
            item.quamtity += 1
            item.save()

        else:
            cart_item = CartItem.objects.create(
            product= product,
            quamtity = 1,
            cart = cart
        )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)


         
                


        # cart_item.quamtity += 1
        
    else:
        cart_item = CartItem.objects.create(
            product= product,
            quamtity = 1,
            cart = cart
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()

            cart_item.variation.add(*product_variation)

                
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quamtity > 1:
            cart_item.quamtity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id , cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    
    cart_item.delete()
    return redirect('cart')

def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quamtity
            quantity += cart_item.quamtity
        tax = (2*total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' :total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total': grand_total

    }
    return render(request,'store/cart.html', context)