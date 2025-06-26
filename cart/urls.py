from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
    path('add/', views.add_cart_item, name='add'),
    path('remove/', views.delete_cart_item, name='remove'),
    path('get-remove-confirmation/<int:item_id>/', views.get_remove_confirmation, name='get_remove_confirmation'),
    path('get-remove-button/<int:item_id>/', views.get_remove_button, name='get_remove_button'),
]