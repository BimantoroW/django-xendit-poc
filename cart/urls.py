from django.urls import path
from . import views
from . import views_api

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
    path('remove/', views.delete_cart_item, name='remove'),
    path('get-remove-confirmation/<int:item_id>/', views.get_remove_confirmation, name='get_remove_confirmation'),
    path('get-remove-button/<int:item_id>/', views.get_remove_button, name='get_remove_button'),

    path('api/add/', views_api.add_cart_item, name='add'),
]