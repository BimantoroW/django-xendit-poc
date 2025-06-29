from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from . import services

@login_required
def cart_view(request):
    cart_items, total_price = services.get_cart_by_user(request.user)

    items = [
        {
            'id': item.id,
            'product': item.course.title,
            'description': item.course.description,
            'price_raw': item.course.price,
            'price_formatted': f'Rp{intcomma(item.course.price)}'
        }
        for item in cart_items
    ]

    return JsonResponse({
        'status': 'success',
        'items': items,
        'total_price_raw': total_price,
        'total_price_formatted': f'Rp{intcomma(total_price)}',
        'item_count': len(items)
    })

@require_POST
@login_required
def cart_add(request):
    course_id = request.POST.get('course_id')
    item_created = services.add_item(request.user, course_id)
    cart_items, _ = services.get_cart_by_user(request.user)
    return JsonResponse({
        'status': 'success',
        'cpurse_id': course_id,
        'item_created': item_created,
        'cart_item_count': cart_items.count()
    })

@require_POST
@login_required
def cart_remove(request):
    item_id = request.POST.get('item_id') 
    services.delete_item(request.user, item_id) 
    return JsonResponse({
        'status': 'success',
        'item_id': item_id,
    })