from django.conf import settings
from django.urls import reverse
import requests
import base64 as b64

def create_invoice(order, request):
    api_key = b64.b64encode(settings.XENDIT_API_KEY.encode()).decode()

    payload = create_invoice_payload(order, request)

    headers = {
        "Authorization": f"Basic {api_key}"
    }

    response = requests.post(f'{settings.XENDIT_API_GATEWAY_URL}/v2/invoices', json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Xendit API Error: ", response.text)
        return None

def create_invoice_payload(order, request):
    success_redirect_url = request.build_absolute_uri(reverse('orders:processing', kwargs={'order_id': order.id}))
    failure_redirect_url = request.build_absolute_uri(reverse('orders:failure'))

    items = []
    for item in order.orderitem_set.all():
        course = item.course
        items.append({
            'name': course.title,
            'quantity': 1,
            'price': course.price
        })

    payload = {
        'external_id': str(order.id),
        'amount': order.total_amount,
        'currency': 'IDR',
        'customer': {
            'given_names': order.user.username,
        },
        'success_redirect_url': success_redirect_url,
        'failure_redirect_url': failure_redirect_url,
        'items': items,
    }

    return payload