from django.shortcuts import render
from .models import *
from django.utils.text import slugify

# Create your views here.

def home(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    if search:
        isbn_books = Book.objects.filter(isbn=search)
        if isbn_books.exists():
            return render(request, 'book_view.html', {
                "title": isbn_books.first().title,
                "book": isbn_books.first(),
                "related_books": Book.objects.filter(genere=isbn_books.first().genere).exclude(id=isbn_books.first().id)[:4],
                "generes" : Genere.objects.all(),
            })
        else:
            books = Book.objects.filter(title__icontains=search)

    elif category:
        books = Book.objects.filter(genere__slug=category)
    elif search:
        books = Book.objects.filter(title__icontains=search)
    else:
        books = Book.objects.all()
    data = {
        "title": "Home",
        "generes" : Genere.objects.all(),
        "books" : books,
    }
    return render(request, 'home.html', data)

def filter(request):
    return render(request, 'filter.html')

def book_view(request, slug):
    book = Book.objects.get(slug=slug)
    related_books = Book.objects.filter(genere=book.genere).exclude(id=book.id)[:4]
    data = {
        "title": book.title,
        "book": book,
        "related_books": related_books,
        "generes" : Genere.objects.all(),
    }
    return render(request, 'book_view.html', data)


def admin_dashboard(request):
    data = {
        "title": "Admin Dashboard",
        "total_books": Book.objects.count(),
        "total_authors": Author.objects.count(),
        "total_genres": Genere.objects.count(),
    }
    return render(request, 'admin/dashboard.html', data)


def admin_books(request): 
    data = {
        "title": "Admin Books",
        "books": Book.objects.all(),
    }
    return render(request, 'admin/books.html', data)


def admin_authors(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")

        if name:
            base_slug = slugify(name)
            slug = base_slug

            # UNIQUE slug banane ke liye loop
            counter = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            Author.objects.create(
                name=name,
                email=email,
                contact=contact,
                slug=slug
            )

    data = {
        "title": "Admin Authors",
        "authors": Author.objects.all().order_by('-id'),
    }

    return render(request, 'admin/authors.html', data)
def admin_genres(request):
    data = {
        "title": "Admin Genres",
        "genres": Genere.objects.all(),
    }
    return render(request, 'admin/genres.html', data)