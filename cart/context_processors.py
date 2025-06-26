from . import services

def cart_context(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = services.get_cart_count_by_user(request.user)

    return {
        'cart_item_count': cart_item_count
    }