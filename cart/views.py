from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from courses.models import Course
from .models import Cart, CartItem
from . import services

@login_required
def cart_page(request):
    cart_items, total_price = services.get_cart_by_user(request.user)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart/cart-details.html', context=context)

@login_required
def get_remove_confirmation(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    return render(request, 'partials/remove-confirmation.html', {'item': item})

@login_required
def get_remove_button(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    return render(request, 'partials/remove-button.html', {'item': item})