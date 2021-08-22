from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', ArticleListView.as_view(), name='products-home'),
    path('api/order/', OrderView.as_view(), name='order'),
    path('api/add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('search/', search, name='search'),
    path('cart/', view_cart, name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('detail_view/<int:pk>/', ArticleDetailView.as_view(), name='detail_view'),
    path('delete_item/<int:pk>/', delete_item, name='delete_item')
]
