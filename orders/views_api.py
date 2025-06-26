from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def get_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return JsonResponse({'status': order.status})