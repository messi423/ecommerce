from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='products-home'),
    path('search/', views.search, name='search'),
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('detail_view/<int:pk>/', views.ArticleDetailView.as_view(), name='detail_view'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item')

]
