from django.urls import path
from . import views_api
from . import views

app_name = 'orders'

urlpatterns = [
    path('receive_callback/', views.receive_callback, name='receive_callback'),
    path('checkout/', views.create_order, name='checkout'),
    path('processing/<int:order_id>/', views.payment_processing, name='processing'),
    path('success/', views.payment_success, name='success'),
    path('failure/', views.payment_failure, name='failure'),

    path('get-status/<int:order_id>/', views_api.get_order_status, name='get_status'),
]