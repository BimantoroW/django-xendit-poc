from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from courses.models import Course
from .models import Cart, CartItem
from . import services

@require_POST
def add_cart_item(request):
    # For htmx purposes. Redirect the user to the login page if they're not authenticated
    if not request.user.is_authenticated:
        login_url = reverse('users:login')
        response = HttpResponse(status=204)
        response['HX-Redirect'] = login_url
        return response

    course_id = request.POST.get('course_id')
    item_created = services.add_item(request.user, course_id)
    if item_created:
        return render(request, 'partials/cart-add-success.html')
    else:
        return render(request, 'partials/already-in-cart.html')

@login_required
def view_cart(request):
    cart_items, total_price = services.get_cart_by_user(request.user)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart/cart-details.html', context=context)

@require_POST
@login_required
def delete_cart_item(request):
    item_id = request.POST.get('item_id') 
    services.delete_item(request.user, item_id) 
    cart_items, total_price = services.get_cart_by_user(request.user)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'partials/cart-contents.html', context)

@login_required
def get_remove_confirmation(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    return render(request, 'partials/remove-confirmation.html', {'item': item})

@login_required
def get_remove_button(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    return render(request, 'partials/remove-button.html', {'item': item})