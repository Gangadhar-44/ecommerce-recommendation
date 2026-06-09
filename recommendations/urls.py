"""
URL configuration for recommendations app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('recommendations/', views.recommendations_page, name='recommendations'),
    path('profile/', views.user_profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('rate/', views.rate_product, name='rate_product'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('purchase/', views.purchase_product, name='purchase_product'),
    path('track/', views.track_behavior, name='track_behavior'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
]
