from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Enrollment
from .models import Order, OrderItem
from cart import services as cs
from . import services
import json

# Quick note: The flow of checking out is
# 1. user clicks checkout
# 2. redirect to xendit
# 3. user pays
# 4. redirect to our waiting page
# 5. poll the get status API until the user's transaction has been confirmed to be paid by Xendit
# 6. redirect to home

@require_POST
@login_required
def create_order(request):
    cart_items, total_price = cs.get_cart_by_user(request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty")
        return redirect('core:home')

    # Create a pending order object
    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_amount=total_price)
        for item in cart_items:
            OrderItem.objects.create(order=order, course=item.course, price=item.course.price)

    invoice_data = services.create_invoice(order, request)

    if invoice_data:
        order.xendit_invoice_id = invoice_data.get('id')
        order.xendit_invoice_url = invoice_data.get('invoice_url')
        order.save()
        cs.clear_cart_by_user(request.user)
        return redirect(order.xendit_invoice_url)
    else:
        messages.error(request, "We could not connect to the payment gateway. Please try again later.")
        return redirect('view_cart')

@require_POST
@csrf_exempt
def receive_callback(request):
    # Always wait until we get confirmation from Xendit before enabling a user's access to a course
    # Don't just blindly trust the system and immediately enable a user's courses after they pay
    # There might be a chance that the payment fails midway through

    callback_token = request.headers.get('X-Callback-Token')
    if callback_token != settings.XENDIT_WEBHOOK_VERIFICATION_TOKEN:
        return HttpResponse(status=403)

    data = json.loads(request.body.decode())
    order_id = data['external_id']
    status = data['status']

    try:
        order = Order.objects.get(id=order_id)
        if status == 'PAID' and order.status != 'PAID':
            order.status = 'PAID'
            order.save()
            with transaction.atomic():
                for item in order.orderitem_set.all():
                    Enrollment.objects.get_or_create(user=order.user, course=item.course)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
        
    return HttpResponse(status=200)

@login_required
def payment_processing(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/payment-processing.html', {'order': order})

def payment_success(request):
    messages.success(request, "Your payment was successful! You now have access to your new courses.")
    return redirect('core:home')

def payment_failure(request):
    messages.error(request, "Your payment could not be completed. Please contact support.")
    return render(request, 'orders/payment_failure.html')
