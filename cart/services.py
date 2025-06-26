from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from courses.models import Course

def get_cart_by_user(user):
    try:
        cart = user.cart
        cart_items = cart.cartitem_set.all().select_related('course')
        total_price = sum(item.course.price for item in cart_items)
    except ObjectDoesNotExist:
        cart_items = []
        total_price = 0
    return cart_items, total_price

def get_cart_count_by_user(user):
    try:
        cart = user.cart
        count = cart.cartitem_set.count()
    except ObjectDoesNotExist:
        count = 0
    return count

def add_item(user, course_id):
    '''
    Raise Http404 exception if course_id does not exist
    '''
    course = get_object_or_404(Course, id=course_id)
    cart, _ = Cart.objects.get_or_create(user=user)
    _, item_created = CartItem.objects.get_or_create(cart=cart, course=course)  
    return item_created

def delete_item(user, item_id):
    '''
    Raise Http404 exception if item_id does not exist
    '''
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Security check so no one can just send a request to this api and delete somebody else's cart item
    if user == cart_item.cart.user:
        cart_item.delete()