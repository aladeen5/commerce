from django.shortcuts import render, get_object_or_404
from .cart import Cart
from ecommercial.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    # Get the cart.
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals})



def cart_add(request):
    # Get the cart.
    cart = Cart(request)
    # Test for POST.
    if request.POST.get('action') == 'post':
        # Get stuff.
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #Look up product in the database.
        product = get_object_or_404(Product, pk=product_id)
        # Save to our session.
        cart.add(product=product, quantity=product_qty)

        # Cet cart quantity.
        cart_quantity = cart.__len__()

        # Return a response.
        # response = JsonResponse({'Product Name': product_name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, 'Product added to cart...')
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff.
        product_id = int(request.POST.get('product_id'))
        # Call delete function in cart.
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, 'Item deleted from shopping cart...')
        return response
        # return redirect('cart:cart_summary')

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff.
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, 'You cart has been updated...')
        return response
        #return redirect('cart:cart_summary')
