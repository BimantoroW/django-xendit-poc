from django.urls import path
from . import views
from . import views_api

app_name = 'cart'

urlpatterns = [
    path('', views.cart_page, name='page'),
    path('get-remove-confirmation/<int:item_id>/', views.get_remove_confirmation, name='get_remove_confirmation'),
    path('get-remove-button/<int:item_id>/', views.get_remove_button, name='get_remove_button'),

    path('api/view/', views_api.cart_view, name='api_view'),
    path('api/add/', views_api.cart_add, name='api_add'),
    path('api/delete/', views_api.cart_remove, name='api_remove'),
]