from django.shortcuts import render, redirect
from .models import Order, Cart


# Create your views here.


def cart_customer_view(request) :
    template_name = "carts/my-cart.html"
    user, _ = Order.objects.new_or_get(request)
    items = user.cart_set.all()
    if request.user.is_authenticated :
        items = Cart.objects.filter(order__user=request.user)
    context = {
        "items" : items,
        "user" : user
    }
    return render(request, template_name, context)

