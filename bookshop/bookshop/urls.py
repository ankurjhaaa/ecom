
from django.contrib import admin
from django.urls import path
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
