from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='marketplace-home'),
    path('cart/', views.cart, name='marketplace-cart'),
    path('checkout/', views.checkout, name='marketplace-checkout'),
    path('faqs/', views.show_faqs, name='faqs'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
]
