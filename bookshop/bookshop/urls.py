
from django.contrib import admin
from django.urls import path
from ecom.checkoutView import addToCart, add_address, cart, checkout, remove_from_cart
from ecom.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('superadmin/', admin.site.urls),
    path("", home, name='home'),
    path('filter/', filter, name='filter'),
    path('book_view/<str:slug>/', book_view, name='book_view'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('admin/',admin_dashboard, name='admin_dashboard'),
    path('admin/books/', admin_books, name='admin_books'),
    path('admin/authors/', admin_authors, name='admin_authors'),
    path('admin/generes/', admin_generes, name='admin_generes'),
    path('admin/coupons/', admin_coupons, name='admin_coupons'),
    path('admin/coupons/<int:coupon_id>/edit/', admin_coupons, name='admin_coupon_edit'),
    path('admin/coupons/<int:coupon_id>/delete/', admin_coupon_delete, name='admin_coupon_delete'),
    
    
    
    path('add_to_cart/<str:slug>/', addToCart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('address/add/', add_address, name='add_address'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
